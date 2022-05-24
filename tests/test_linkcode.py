import pytest
from bs4 import BeautifulSoup
from sphinx.application import Sphinx


def _parse_rule_link(rule_name: str, soup: BeautifulSoup):
    return soup.find("dt", id=f"rule-{rule_name}").find("a", class_="reference external").get("href").split("#L")


@pytest.mark.sphinx('html', testroot='docs')
def test_source_links(app: Sphinx):
    SNAKEFILE_URL = "https://github.com/smutch/snakedoc/blob/master/snakedoc/tests/workflow/Snakefile"
    app.builder.build_all()
    index = app.outdir / "index.html"
    assert index.exists()

    with open(index, "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    for rule_name, expected in (("basic", 5), ("follows_basic", 26), ("also_follows_basic", 38), ("the_end", 50)):
        url, lineno = _parse_rule_link(rule_name, soup)
        assert url == SNAKEFILE_URL
        assert int(lineno) == expected
