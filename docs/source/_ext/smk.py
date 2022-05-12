from collections import defaultdict
from typing import Any, Dict

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.directives import ObjectDescription, SphinxDirective
from sphinx.domains import Domain, Index
from sphinx.roles import XRefRole
from sphinx.util.docfields import Field, GroupedField
from sphinx.util.docutils import switch_source_input
from sphinx.util.nodes import make_refnode, nested_parse_with_titles


class RuleDirective(ObjectDescription):
    """A custom directive that describes a Snakemake rule."""

    has_content = True
    required_arguments = 1
    priority = 0
    option_spec = {"source": directives.unchanged}

    doc_field_types = [
        GroupedField("input", label="Inputs", names=("input",), can_collapse=True),
        GroupedField("output", label="Outputs", names=("output",), can_collapse=True),
        GroupedField(
            "param", label="Params", names=("param", "parameter"), can_collapse=True
        ),
        Field("conda", label="Conda", names=("conda",), has_arg=False),
        Field("log", label="Log", names=("log",), has_arg=False),
        Field("resources", label="resources", names=("resources",), has_arg=False),
    ]

    def handle_signature(self, sig, signode):
        signode += addnodes.desc_name(text=sig, source=self.options.get("source", ""))
        return sig

    def add_target_and_index(self, name_cls, sig, signode):
        signode["ids"].append("rule" + "-" + sig)
        breakpoint()
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

        # sort the list of recipes in alphabetical order
        # TODO: Have this in logical order
        rules = self.domain.get_objects()
        rules = sorted(rules, key=lambda rule: rule[0])

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


class SmkDomain(Domain):

    name = "smk"
    label = "Snakemake"
    roles = {"ref": XRefRole()}
    directives = {"rule": RuleDirective}
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
