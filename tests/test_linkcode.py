import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from sphinx.application import Sphinx

from snakedoc import linkcode

RULE_PATTERN = re.compile(r"^\s*rule\s+(\S+)\s*:\s*$")


def _parse_rule_link(rule_name: str, soup: BeautifulSoup):
    return soup.find("dt", id=f"rule-{rule_name}").find("a", class_="reference external").get("href").split("#L")


def test_smk_linkcode_resolve():
    domain = None
    info = {"source": "./snake.smk", "basepath": "./", "baseurl": "https://blaa/", "linesep": "-"}
    assert linkcode.smk_linkcode_resolve(domain, info) == f"{info['baseurl']}snake.smk"

    info["source"] += ":22"
    assert linkcode.smk_linkcode_resolve(domain, info) == f"{info['baseurl']}snake.smk{info['linesep']}22"

    info["source"] += ":55"
    with pytest.raises(linkcode.SmkLinkcodeError):
        linkcode.smk_linkcode_resolve(domain, info)

    info["source"] = "/snake.smk"
    with pytest.raises(linkcode.SmkLinkcodeError):
        linkcode.smk_linkcode_resolve(domain, info)

    info["source"] = ""
    assert linkcode.smk_linkcode_resolve(domain, info) == ""


@pytest.mark.sphinx('html', testroot='docs')
def test__set_resolve_target(app: Sphinx):
    env = app.builder.env

    def dummy(domain, info):
        pass

    assert linkcode._set_resolve_target(env) == linkcode.smk_linkcode_resolve
    env.config["smk_linkcode_resolve"] = dummy
    assert linkcode._set_resolve_target(env) == dummy


@pytest.mark.sphinx('html', testroot='docs')
def test__set_basepath_baseurl(app: Sphinx):
    env = app.builder.env
    basepath, baseurl = linkcode._set_basepath_baseurl(env)
    assert baseurl == env.config.smk_linkcode_mapping[1]

    with_slash = baseurl
    env.config.smk_linkcode_mapping = (basepath, baseurl[:-1])
    basepath, baseurl = linkcode._set_basepath_baseurl(env)
    assert baseurl == with_slash


@pytest.mark.sphinx('html', testroot='docs')
def test_source_links(app: Sphinx):
    SNAKEFILE_URL = "https://github.com/smutch/test/blob/master/workflow/Snakefile"
    snakefile_path = Path(app.confdir) / "workflow/Snakefile"

    app.builder.build_all()
    index = app.outdir / "index.html"
    assert index.exists()

    with open(index, "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    snakefile = snakefile_path.read_text('utf-8').splitlines(keepends=False)
    for rule_name in ("basic", "follows_basic", "also_follows_basic", "the_end"):
        url, lineno = _parse_rule_link(rule_name, soup)
        assert url == SNAKEFILE_URL

        expected = -1
        for ii, line in enumerate(snakefile):
            match = RULE_PATTERN.search(line)
            if match and match.group(1) == rule_name:
                expected = ii + 1
                break
        else:
            raise ValueError(f"Failed to locate rule {rule_name}")
        assert int(lineno) == expected, f"Line number for rule {rule_name} does not match expectation"
