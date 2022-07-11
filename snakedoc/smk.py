import logging
from collections import defaultdict
from enum import Enum
from pathlib import Path
from textwrap import dedent, indent
from typing import Any, Dict, Mapping

import snakemake
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.directives import ObjectDescription, SphinxDirective
from sphinx.domains import Domain, Index
from sphinx.roles import XRefRole
from sphinx.util.docfields import Field, GroupedField
from sphinx.util.docutils import switch_source_input
from sphinx.util.nodes import make_refnode, nested_parse_with_titles

from . import linkcode

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class RuleType(Enum):
    RULE = "rule"
    CHECKPOINT = "checkpoint"


class RuleDirective(ObjectDescription):
    """A custom directive that describes a Snakemake rule."""

    has_content = True
    required_arguments = 1
    priority = 0
    option_spec = {"source": directives.unchanged}
    rule_type = RuleType.RULE

    doc_field_types = [
        GroupedField("input", label="Input", names=("input", "in"), can_collapse=True),
        GroupedField("output", label="Output", names=("output", "out"), can_collapse=True),
        GroupedField("param", label="Params", names=("param", "parameter"), can_collapse=True),
        GroupedField("resource", label="Resources", names=("resource",), can_collapse=True),
        GroupedField("config", label="Config", names=("config", "conf"), can_collapse=True),
        Field("conda", label="Conda", names=("conda",)),
        Field("log", label="Log", names=("log",), has_arg=False),
        Field("notebook", label="Notebook", names=("notebook"), has_arg=False),
        Field("shell", label="Shell", names=("shell"), has_arg=False),
        Field(
            "script", label="Script", names=("script"), has_arg=False
        ),  # TODO: link to script on github automatically?
        Field("run", label="Run", names=("run"), has_arg=False),
        Field("wildcard_constraints", label="Wildcard constraints", names=("wildcard_constraints"), has_arg=False),
        Field("threads", label="Threads", names=("threads"), has_arg=False),
        Field("priority", label="Priority", names=("priority"), has_arg=False),
        Field("retires", label="Retires", names=("retires"), has_arg=False),
        Field("benchmark", label="Benchmark", names=("benchmark", "bench"), has_arg=False),
        Field("group", label="Group", names=("group", "grp"), has_arg=False),
        Field("default_target", label="Default target", names=("default_target"), has_arg=False),
    ]

    def handle_signature(self, sig, signode):
        signode.insert(1, addnodes.desc_type(text=f"{self.rule_type.value.capitalize()} "))
        signode += addnodes.desc_name(text=sig, source=self.options.get("source", ""))
        return sig

    def add_target_and_index(self, name_cls, sig, signode):
        signode["ids"].append("rule" + "-" + sig)
        signode.attributes["source"] = self.options.get("source", None)
        smk = self.env.get_domain("smk")
        smk.add_rule(sig, self.rule_type)


class CheckpointDirective(RuleDirective):
    rule_type = RuleType.CHECKPOINT


class RuleIndex(Index):
    """A custom index that creates an rule index."""

    name = "rule"
    localname = "Snakemake Rules"
    shortname = "Rule"

    def generate(self, docnames=None):
        content = defaultdict(list)

        rules = self.domain.get_objects()

        # sort the list of recipes in alphabetical order
        # rules = sorted(rules, key=lambda rule: rule[0])

        # generate the expected output, shown below, from the above using the
        # first letter of the recipe as a key to group thing
        #
        # name, subtype, docname, anchor, extra, qualifier, description
        for _name, dispname, typ, docname, anchor, _priority in rules:
            content[dispname[0].lower()].append((dispname, 0, docname, anchor, docname, "", typ))

        # convert the dict to the sorted list of tuples expected
        content = sorted(content.items())

        return content, True


class AutoDocDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 1
    _docstring_types = None
    option_spec = {
        'configfile': directives.path,
        'config': directives.unchanged,
    }

    def _extract_rules(self):
        configfile = self.options.get("configfile", None)
        config_args = None
        if "config" in self.options:
            config_args = {}
            for line in self.options["config"].splitlines():
                try:
                    k, v = map(str.strip, line.split("=", 1))
                    config_args[k] = v
                except ValueError as err:
                    raise Exception("The smk:autodoc config option must be made up of key=value entries") from err

        workflow = snakemake.Workflow(
            self.arguments[0],
            overwrite_configfiles=configfile,
            config_args=config_args,
            rerun_triggers=snakemake.RERUN_TRIGGERS,
        )
        workflow.config.update(config_args or {})
        workflow.include(self.arguments[0], overwrite_default_target=True)
        workflow.check()

        if len(self.arguments) > 1:
            rule = self.arguments[1]
            workflow._rules = {rule: workflow._rules[rule]}

        return workflow._rules

    def _gen_docs(viewlist: ViewList, rules: Mapping[str, snakemake.rules.Rule]):
        for rule in rules.values():
            lines = []
            lineno = rule.workflow.linemaps[rule.snakefile][rule.lineno]
            rule_type = "rule" if not rule.is_checkpoint else "checkpoint"
            lines.extend(
                [f".. smk:{rule_type}:: {rule.name}", f"   :source: {Path(rule.snakefile).resolve()}:{lineno}", ""]
            )

            if rule.docstring is not None:
                docstring = indent(dedent(rule.docstring), "   ")
                lines.extend(docstring.splitlines())
                lines.append("")

            if rule.conda_env:
                lines.extend(
                    [
                        "   :conda:",
                        "     .. code-block:: yaml",
                        "",
                    ]
                )
                with open(rule.conda_env.file, "r") as fp:
                    env = indent(fp.read(), "         ")
                lines.extend(env.splitlines(keepends=False))
                lines.append("")

            # NOTE: Making a copy of rule.resources here to not break things later
            resources = {}
            resources.update(rule.resources)
            resources.pop("tmpdir")
            if (
                any(callable(v) for v in resources.values())
                or resources["_cores"] > 1
                or resources["_nodes"] > 1
                or len(resources) > 2
            ):
                lines.extend([f"   :resource {k.strip('_')}: {v}" for k, v in resources.items()])
            lines.append("")

            lines.extend(["", "|", ""])

            logger.debug(f"smk::autodoc generated this for rule {rule.name}:")
            logger.debug("\n".join(lines))

            for line in lines:
                viewlist.append(line, rule.snakefile, lineno)

    def run(self):
        result = ViewList()

        rules = self._extract_rules()
        AutoDocDirective._gen_docs(result, rules)

        # Parse the extracted reST
        with switch_source_input(self.state, result):
            node = nodes.section()
            nested_parse_with_titles(self.state, result, node)

        return node.children


class SmkDomain(Domain):

    name = "smk"
    label = "Snakemake"
    roles = {"ref": XRefRole()}
    directives = {"rule": RuleDirective, "checkpoint": CheckpointDirective, "autodoc": AutoDocDirective}
    indices = {
        RuleIndex,
    }
    initial_data = {
        "rules": [],  # object list
    }

    def get_full_qualified_name(self, node):
        return "{}.{}".format("rule", node.arguments[0])

    def get_objects(self):
        for obj in self.data["rules"]:
            yield (obj)

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        match = [(docname, anchor) for name, sig, typ, docname, anchor, prio in self.get_objects() if sig == target]

        if len(match) > 0:
            todocname = match[0][0]
            targ = match[0][1]

            return make_refnode(builder, fromdocname, todocname, targ, contnode, targ)
        else:
            print("Awww, found nothing")
            return None

    def add_rule(self, dispname, rule_type: RuleType):  # , input, output, params, log, resources, shell, script):
        """Add a new rule to the domain."""
        name = "{}.{}".format("rule", dispname)
        anchor = "rule-{}".format(dispname)

        # name, dispname, type, docname, anchor, priority
        self.data["rules"].append((name, dispname, rule_type.value.capitalize(), self.env.docname, anchor, 0))


def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension("sphinx.ext.autodoc")
    app.add_domain(SmkDomain)

    app.add_config_value("smk_linkcode_resolve", None, "")
    app.add_config_value("smk_linkcode_baseurl", "", "")
    app.add_config_value("smk_linkcode_linesep", "#L", "")
    app.connect("doctree-read", linkcode.doctree_read)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
