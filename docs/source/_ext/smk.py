import logging
from collections import defaultdict
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

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class RuleDirective(ObjectDescription):
    """A custom directive that describes a Snakemake rule."""

    has_content = True
    required_arguments = 1
    priority = 0
    option_spec = {"source": directives.unchanged}

    doc_field_types = [
        GroupedField("input", label="input", names=("input",), can_collapse=True),
        GroupedField("output", label="output", names=("output",), can_collapse=True),
        GroupedField(
            "param", label="params", names=("param", "parameter"), can_collapse=True
        ),
        Field("conda", label="conda", names=("conda",)),
        Field("log", label="log", names=("log",), has_arg=False),
        Field("resources", label="resources", names=("resources",), has_arg=False),
    ]

    def handle_signature(self, sig, signode):
        signode += addnodes.desc_name(text=sig, source=self.options.get("source", ""))
        return sig

    def add_target_and_index(self, name_cls, sig, signode):
        signode["ids"].append("rule" + "-" + sig)
        signode.attributes["source"] = self.options.get("source", None)
        smk = self.env.get_domain("smk")
        smk.add_rule(sig)


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
            content[dispname[0].lower()].append(
                (dispname, 0, docname, anchor, docname, "", typ)
            )

        # convert the dict to the sorted list of tuples expected
        content = sorted(content.items())

        return content, True


class AutoDocDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    _docstring_types = None

    def _extract_rules(self):
        workflow = snakemake.Workflow(self.arguments[0])
        workflow.include(self.arguments[0], overwrite_default_target=True)
        workflow.check()
        return workflow.rules.mapping

    def _gen_docs(viewlist: ViewList, rules: Mapping[str, snakemake.rules.Rule]):
        for rule in rules.values():
            lines = []
            lines.extend(
                [
                    f".. smk:rule:: {rule.name}",
                    f"   :source: {Path(rule.snakefile).resolve()}:{rule.lineno}",
                ]
            )

            if rule.docstring is not None:
                docstring = indent(dedent(rule.docstring), "   ")
                lines.extend(docstring.splitlines())

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

            if rule.resources["_cores"] > 1 or rule.resources["_nodes"] > 1:
                resources = ",".join(
                    (
                        f"{k.lstrip('_')}={v}"
                        for k, v in rule.resources.items()
                        if k != "tmpdir"
                    )
                )
                lines.append(f"   :resources: {resources}")

            lines.extend(["", "|", ""])

            logger.debug(f"smk::autodoc generated this for rule {rule.name}:")
            logger.debug("\n".join(lines))

            for line in lines:
                viewlist.append(line, rule.snakefile, rule.lineno)

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
    directives = {"rule": RuleDirective, "autodoc": AutoDocDirective}
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
        match = [
            (docname, anchor)
            for name, sig, typ, docname, anchor, prio in self.get_objects()
            if sig == target
        ]

        if len(match) > 0:
            todocname = match[0][0]
            targ = match[0][1]

            return make_refnode(builder, fromdocname, todocname, targ, contnode, targ)
        else:
            print("Awww, found nothing")
            return None

    def add_rule(
        self, dispname
    ):  # , input, output, params, log, resources, shell, script):
        """Add a new rule to the domain."""
        name = "{}.{}".format("rule", dispname)
        anchor = "rule-{}".format(name)

        # name, dispname, type, docname, anchor, priority
        self.data["rules"].append((name, dispname, "Rule", self.env.docname, anchor, 0))


def setup(app: Sphinx) -> Dict[str, Any]:
    app.setup_extension("sphinx.ext.autodoc")
    app.add_domain(SmkDomain)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
