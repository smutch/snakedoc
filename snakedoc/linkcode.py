from pathlib import Path
from typing import Callable, Set

import docutils
from docutils import nodes
from docutils.nodes import Node
from sphinx import addnodes
from sphinx.application import BuildEnvironment, Sphinx
from sphinx.errors import SphinxError
from sphinx.locale import _


class SmkLinkcodeError(SphinxError):
    category = "linkcode error"


def smk_linkcode_resolve(domain, info):
    if len(info["source"]) == 0:
        return ""

    parts = info["source"].split(":")
    if len(parts) == 2:
        filename, lineno = parts
    elif len(parts) == 1:
        filename = parts[0]
        lineno = None
    else:
        raise SmkLinkcodeError(f"Failed to parse source: {info['source']}")
    try:
        filename = str(Path(filename).relative_to(info['basepath']))
    except ValueError as err:
        raise SmkLinkcodeError(
            f"Rule lists {filename} as it's source, but this is not relative to {info['basepath']}"
        ) from err

    return f"{info['baseurl']}{filename}{info['linesep']+lineno if lineno else ''}"


def _set_resolve_target(env: BuildEnvironment) -> Callable:
    resolve_target = getattr(env.config, "smk_linkcode_resolve", None)
    if env.config.smk_linkcode_resolve is None:
        resolve_target = smk_linkcode_resolve
    else:
        resolve_target = env.config.smk_linkcode_resolve
    return resolve_target


def _set_basepath_baseurl(env: BuildEnvironment) -> (str, str):
    basepath, baseurl = getattr(env.config, "smk_linkcode_mapping", ("", ""))
    if len(baseurl) > 0 and baseurl[-1] != "/":
        baseurl = f"{baseurl}/"
    return basepath, baseurl


def doctree_read(app: Sphinx, doctree: Node) -> None:
    env = app.builder.env

    resolve_target = _set_resolve_target(env)
    basepath, baseurl = _set_basepath_baseurl(env)
    linesep = getattr(env.config, "smk_linkcode_linesep", "#L")

    domain_keys = {
        "smk": ["source"],
    }

    # TODO: Remove monkeypatch when https://github.com/sphinx-doc/sphinx/pull/10597 is released in Sphinx v5.0.3
    if docutils.__version_info__ < (0, 18):  # pragma: no cover

        def findall(self, *args, **kwargs):
            return iter(self.traverse(*args, **kwargs))

        Node.findall = findall

    for objnode in list(doctree.findall(addnodes.desc)):
        domain = objnode.get("domain")
        uris: Set[str] = set()
        for signode in objnode:
            if not isinstance(signode, addnodes.desc_signature):
                continue

            # Convert signode to a specified format
            info = {}
            for key in domain_keys.get(domain, []):
                value = signode.get(key)
                if not value:
                    value = ""
                info[key] = value
            if not info:  # pragma: no cover
                continue

            # Call user code to resolve the link
            info["baseurl"] = baseurl
            info["basepath"] = basepath
            info["linesep"] = linesep
            uri = resolve_target(domain, info)
            if not uri:
                # no source
                continue

            if uri in uris or not uri:  # pragma: no cover
                # only one link per name, please
                continue
            uris.add(uri)

            inline = nodes.inline("", _("[source]"), classes=["viewcode-link"])
            onlynode = addnodes.only(expr="html")
            onlynode += nodes.reference("", "", inline, internal=False, refuri=uri)
            signode += onlynode
