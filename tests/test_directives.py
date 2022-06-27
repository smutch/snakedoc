import pytest
from bs4 import BeautifulSoup, element
from sphinx.application import Sphinx


def _build_and_blend(app: Sphinx) -> str:
    app.builder.build_all()
    index = app.outdir / "index.html"
    assert index.exists()
    with open(index, "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")
    return soup


def _get_rule(rule_name: str, soup: BeautifulSoup) -> str:
    return " ".join(
        list(filter(lambda dl: dl.find("dt", id=f"rule-{rule_name}"), soup.find_all("dl")).__next__().stripped_strings)
    )


@pytest.mark.sphinx('html', testroot='docs')
def test_rule_directive(app: Sphinx):
    soup = _build_and_blend(app)
    rule = _get_rule("handwritten", soup)

    assert "Input : a.txt" in rule
    assert "Output : b.txt" in rule

    assert "params : c – set c" in rule
    assert "d – set d" in rule

    assert "Conda : channels : - conda-forge" in rule

    assert "resources : mem_mb – 2" in rule
    assert "config : handwritten.a – A dummy config parameter used in this rule" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_checkpoint(app: Sphinx):
    soup = _build_and_blend(app)
    rule = _get_rule("hw_checkpoint", soup)

    assert "Input : a.txt" in rule
    assert "Output : b.txt" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_autodoc_directive(app: Sphinx):
    soup = _build_and_blend(app)
    rule = _get_rule("follows_basic", soup)

    assert "resources : cores – 1" in rule
    assert "nodes – 1" in rule
    assert "mem_mb – 2" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_autodoc_single_file(app: Sphinx):
    soup = _build_and_blend(app)
    rule = _get_rule("other", soup)

    assert "Input : an input file" in rule
    assert "Output : an output file" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_autodoc_single_rule(app: Sphinx):
    soup = _build_and_blend(app)
    rule = _get_rule("other", soup)

    assert "Input : an input file" in rule
    assert "Output : an output file" in rule
