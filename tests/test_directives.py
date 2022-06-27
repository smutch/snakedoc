import pytest
from bs4 import BeautifulSoup, element
from sphinx.application import Sphinx


def _get_rule(rule_name: str, soup: BeautifulSoup) -> element.Tag:
    return filter(lambda dl: dl.find("dt", id=f"rule-{rule_name}"), soup.find_all("dl")).__next__()


@pytest.mark.sphinx('html', testroot='docs')
def test_rule_directive(app: Sphinx):
    app.builder.build_all()
    index = app.outdir / "index.html"
    assert index.exists()

    with open(index, "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    rule = _get_rule("handwritten", soup)
    strings = " ".join(list(rule.stripped_strings))

    assert "Input : a.txt" in strings
    assert "Output : b.txt" in strings

    assert "params : c – set c" in strings
    assert "d – set d" in strings

    print(strings)
    assert "Conda : channels : - conda-forge" in strings

    assert "resources : mem_mb – 2" in strings
    assert "config : handwritten.a – A dummy config parameter used in this rule" in strings


@pytest.mark.sphinx('html', testroot='docs')
def test_checkpoint(app: Sphinx):
    app.builder.build_all()
    index = app.outdir / "index.html"
    assert index.exists()

    with open(index, "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    rule = _get_rule("hw_checkpoint", soup)
    strings = " ".join(list(rule.stripped_strings))

    assert "Input : a.txt" in strings
    assert "Output : b.txt" in strings


@pytest.mark.sphinx('html', testroot='docs')
def test_autodoc_directive(app: Sphinx):
    app.builder.build_all()
    index = app.outdir / "index.html"
    assert index.exists()

    with open(index, "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    rule = _get_rule("follows_basic", soup)
    strings = " ".join(rule.stripped_strings)

    assert "resources : cores – 1" in strings
    assert "nodes – 1" in strings
    assert "mem_mb – 2" in strings
