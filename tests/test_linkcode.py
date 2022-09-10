import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from sphinx.application import Sphinx

RULE_PATTERN = re.compile(r"^\s*rule\s+(\S+)\s*:\s*$")


def _parse_rule_link(rule_name: str, soup: BeautifulSoup):
    return soup.find("dt", id=f"rule-{rule_name}").find("a", class_="reference external").get("href").split("#L")


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
