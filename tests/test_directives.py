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
    strings = list(rule.stripped_strings)

    assert ['Input', 'a.txt'] <= strings
    assert ['Ouput', 'b.txt'] <= strings
    assert ['Params', 'c', '– set', 'c'] <= strings
    assert ['d', '– set', 'd'] <= strings
    assert ['Conda', 'channels', ':', '-', 'conda-forge'] <= strings
