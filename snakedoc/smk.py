import logging
from collections import defaultdict
from enum import Enum
from functools import reduce
from pathlib import Path
from textwrap import dedent, indent
from typing import Any, Dict, List, Mapping, Tuple, cast

import snakemake
from docutils import nodes
from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.parsers.rst.states import Inliner
from docutils.statemachine import ViewList
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.directives import ObjectDescription, SphinxDirective
from sphinx.domains import Domain, Index, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.errors import SphinxError
from sphinx.ext.napoleon import Config
from sphinx.ext.napoleon.docstring import GoogleDocstring
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


class ConfigField(GroupedField):
    def make_field(
        self,
        types: Dict[str, List[Node]],
        domain: str,
        items: Tuple,
        env: BuildEnvironment = None,
        inliner: Inliner = None,
        location: Node = None,
    ) -> nodes.field:
        fieldname = nodes.field_name('', self.label)
        listnode = self.list_type()
        for fieldarg, content in items:
            par = nodes.paragraph()
            par.extend(
                self.make_xrefs(
                    self.rolename,
                    domain,
                    fieldarg,
                    addnodes.literal_strong,
                    env=env,
                    inliner=inliner,
                    location=location,
                )
            )
            par += nodes.Text(' -- ')
            par += content
            listnode += nodes.list_item('', par)

        if len(items) == 1 and self.can_collapse:
            list_item = cast(nodes.list_item, listnode[0])
            fieldbody = nodes.field_body('', list_item[0])
            return nodes.field('', fieldname, fieldbody)

        fieldbody = nodes.field_body('', listnode)
        return nodes.field('', fieldname, fieldbody)


class RuleDirective(ObjectDescription):
    """A custom directive that describes a Snakemake rule."""

    has_content = True
    required_arguments = 1
    priority = 0
    option_spec = {"source": directives.unchanged}
    rule_type = RuleType.RULE

    doc_field_types = [
        GroupedField("input", label="Input", names=("input", "Input", "in", "inputs", "Inputs"), can_collapse=True),
        GroupedField("output", label="Output", names=("output", "out", "outputs", "Outputs"), can_collapse=True),
        GroupedField(
            "param",
            label="Params",
            names=("param", "Param", "parameter", "Parameter", "params", "Params", "parameters", "Parameters"),
            can_collapse=True,
        ),
        GroupedField(
            "resource", label="Resources", names=("resource", "resources", "Resource", "Resources"), can_collapse=True
        ),
        ConfigField(
            "config", label="Config", names=("config", "Config", "configs", "Configs", "conf"), can_collapse=True
        ),
        Field("conda", label="Conda", names=("conda", "Conda")),
        Field("log", label="Log", names=("log", "Log"), has_arg=False),
        Field("notebook", label="Notebook", names=("notebook", "Notebook"), has_arg=False),
        Field("shell", label="Shell", names=("shell", "Shell"), has_arg=False),
        Field(
            "script", label="Script", names=("script", "Script"), has_arg=False
        ),  # TODO: link to script on github automatically?
        Field("run", label="Run", names=("run", "Run"), has_arg=False),
        Field(
            "wildcard_constraints",
            label="Wildcard constraints",
            names=("wildcard_constraints", "Wildcard_Constraints", "wildcard constraints", "Wildcard Constraints"),
            has_arg=False,
        ),
        Field("threads", label="Threads", names=("threads", "Threads"), has_arg=False),
        Field("priority", label="Priority", names=("priority", "Priority"), has_arg=False),
        Field("retires", label="Retires", names=("retires", "Retries"), has_arg=False),
        Field("benchmark", label="Benchmark", names=("benchmark", "Benchmark", "bench"), has_arg=False),
        Field("group", label="Group", names=("group", "Group", "grp"), has_arg=False),
        Field(
            "default_target",
            label="Default target",
            names=("default_target", "Default_Target", "default target", "Default Target"),
            has_arg=False,
        ),
    ]

    def transform_content(self, contentnode: addnodes.desc_content) -> None:
        if hasattr(self.env, "_workflow"):
            for node in contentnode.traverse():
                if node.tagname == 'field' and node[0][0].astext().lower().startswith("conf"):
                    key = node[0][0].split(" ")[1]
                    value = reduce(dict.get, key.split("."), self.env._workflow.config)

                    default = nodes.paragraph()

                    prefix = nodes.emphasis()
                    prefix += nodes.Text("default: ")

                    value_node = nodes.literal()
                    value_node += nodes.Text(f"{value}")

                    # suffix = nodes.emphasis()
                    # suffix += nodes.Text(")")

                    for new_node in (prefix, value_node):
                        default += new_node

                    node[1][0] += default

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
    """A custom Index for rules."""

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


class SmkAutoDocError(SphinxError):
    category = "autodoc error"


def _parse_custom_params_style_section(self, section: str) -> List[str]:
    if self._config.napoleon_use_param and section.lower() in ('config', 'conf'):
        # Allow to declare multiple parameters at once (ex: x, y: int)
        fields = self._consume_fields(multiple=True)
        return self._format_docutils_params(fields, field_role=section.lower())
    else:
        fields = self._consume_fields()
        return self._format_fields(section.lower(), fields)


class AutoDocDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 20  # NOTE: Totally arbitrary number!
    _docstring_types = None
    option_spec = {
        'configfile': directives.path,
        'config': directives.unchanged,
    }

    def _extract_rules(self):
        configfiles = self.options.get("configfile", self.env.config["smk_configfile"])
        if configfiles is not None:
            if isinstance(configfiles, (str, Path)):  # pragma: no cover
                configfiles = [configfiles]
            for ii, cf in enumerate(configfiles):
                cf = Path(cf)
                if not cf.is_absolute():
                    configfiles[ii] = Path(self.env.app.confdir) / cf

        config_args = {}
        if "config" in self.options:
            for line in self.options["config"].splitlines():
                try:
                    k, v = map(str.strip, line.split("=", 1))
                    config_args[k] = v
                except ValueError as err:
                    raise SmkAutoDocError("The smk:autodoc config option must be made up of key=value entries") from err

        config = {}
        if configfiles is not None:
            for configfile in configfiles:
                snakemake.utils.update_config(config, snakemake.load_configfile(configfile))
        snakemake.utils.update_config(config, self.env.config["smk_config"])
        snakemake.utils.update_config(config, config_args)

        snakefile = self.arguments[0]
        snakefile = Path(self.env.app.srcdir) / Path(snakefile)

        workflow = snakemake.Workflow(
            snakefile,
            config_args=config_args,
            overwrite_configfiles=configfiles,
            overwrite_config=config,
            rerun_triggers=snakemake.RERUN_TRIGGERS,
        )
        workflow.include(snakefile, overwrite_default_target=True)
        workflow.check()

        if len(self.arguments) > 1:
            workflow._rules = {k: workflow._rules[k] for k in self.arguments[1:]}

        self.env._workflow = workflow

        return workflow._rules

    def _gen_docs(self, viewlist: ViewList, rules: Mapping[str, snakemake.rules.Rule]):
        for rule in rules.values():
            lines = []
            lineno = rule.workflow.linemaps[rule.snakefile][rule.lineno]
            rule_type = "rule" if not rule.is_checkpoint else "checkpoint"
            snakefile = Path(rule.snakefile).resolve()
            lines.extend([f".. smk:{rule_type}:: {rule.name}", f"   :source: {snakefile}:{lineno}", ""])

            if rule.docstring is not None:
                config = Config(
                    napoleon_use_param=True,
                    napoleon_custom_sections=[
                        (name, "params_style")
                        for field in RuleDirective.doc_field_types
                        if isinstance(field, (GroupedField, ConfigField))
                        for name in field.names
                    ],
                )
                GoogleDocstring._parse_custom_params_style_section = _parse_custom_params_style_section
                docstring = indent(str(GoogleDocstring(dedent(f"    {rule.docstring}"), config=config)), "   ")
                lines.extend(docstring.splitlines())
                lines.append("")

            if rule.conda_env:
                lines.extend(
                    [
                        "   :Conda:",
                        "     .. code-block:: yaml",
                        "   ",
                    ]
                )
                fname = rule.conda_env if isinstance(rule.conda_env, str) else rule.conda_env.file
                with open(snakefile.parent / fname, "r") as fp:
                    env = indent(fp.read(), "         ")
                lines.extend(env.splitlines(keepends=False))
                lines.append("")

            # # NOTE: Making a copy of rule.resources here to not break things later
            # resources = {}
            # resources.update(rule.resources)
            # resources.pop("tmpdir")
            # if (
            #     any(callable(v) for v in resources.values())
            #     or resources["_cores"] > 1
            #     or resources["_nodes"] > 1
            #     or len(resources) > 2
            # ):
            #     lines.extend([f"   :resource {k.strip('_')}: {v}" for k, v in resources.items()])
            # lines.append("")

            lines.extend(["", "|", ""])

            logger.debug(f"smk::autodoc generated this for rule {rule.name}:")
            logger.debug("\n".join(lines))

            for line in lines:
                viewlist.append(line, rule.snakefile, lineno)

    def run(self):
        result = ViewList()

        rules = self._extract_rules()
        AutoDocDirective._gen_docs(self, result, rules)

        # Parse the extracted reST
        with switch_source_input(self.state, result):
            node = nodes.section()
            nested_parse_with_titles(self.state, result, node)

        # Sphinx wants to pickle the environment and we can't pickle the workflow object so just remove it
        del self.env._workflow

        return node.children


class SmkDomain(Domain):
    name = "smk"
    label = "Snakemake"
    roles = {"ref": XRefRole()}
    directives = {"rule": RuleDirective, "checkpoint": CheckpointDirective, "autodoc": AutoDocDirective}
    object_types = {"Rule": ObjType("rule", RuleDirective, CheckpointDirective)}
    indices = {
        RuleIndex,
    }
    initial_data = {
        "rules": [],  # object list
    }

    # def get_full_qualified_name(self, node):
    #     return "{}.{}".format("rule", node.arguments[0])

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

    def add_rule(self, dispname: str, rule_type: RuleType):
        """Add a new rule to the domain."""
        name = f"rule.{dispname}"
        anchor = f"rule-{dispname}"

        # name, dispname, type, docname, anchor, priority
        self.data["rules"].append((name, dispname, rule_type.value.capitalize(), self.env.docname, anchor, 0))


def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension("sphinx.ext.autodoc")
    app.add_domain(SmkDomain)

    app.add_config_value("smk_linkcode_resolve", None, "env")
    app.add_config_value("smk_linkcode_mapping", ("", ""), "env")
    app.add_config_value("smk_linkcode_linesep", "#L", "env")
    app.add_config_value("smk_config", {}, "env")
    app.add_config_value("smk_configfile", None, "env")

    app.connect("doctree-read", linkcode.doctree_read)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
