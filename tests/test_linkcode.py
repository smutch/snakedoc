import re

import pytest
from bs4 import BeautifulSoup
from sphinx.application import Sphinx

# TODO: make building the docs testroot a fixture
# TODO: don't hardcode url in tests


@pytest.mark.sphinx('html', testroot='docs')
def test_source_links(app: Sphinx, status, warning):
    app.builder.build_all()
    index = app.outdir / "index.html"
    assert index.exists()

    with open(index, "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    url, lineno = soup.find("dt", id="rule-basic").find("a", class_="reference external").get("href").split("#L")
    assert url == "https://github.com/smutch/snakedoc/blob/master/snakedoc/tests/workflow/Snakefile"
    assert int(lineno) == 5
