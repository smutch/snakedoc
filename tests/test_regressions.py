import re
import sys

import pytest
import sphinx
from sphinx.application import Sphinx

# Note that we stop checking the body from the footer onwards. This is because the footer contains the exact versions of
# the Sphinx etc. which we don't care about and will break the testss with dependabot PRs etc.
body_pattern = re.compile(r'<body>.*<div class="footer">', re.DOTALL)


@pytest.mark.skipif(
    sphinx.version_info[0] < 7 or sys.version_info < (3, 9), reason="regression test is Sphinx version dependent (>=7)"
)
@pytest.mark.sphinx('html', testroot='docs')
def test_build(data_regression, app: Sphinx):
    app.builder.build_all()
    assert (app.outdir / "index.html").exists()

    data = {}
    for page in ('index', 'smk-rule'):
        data[page] = body_pattern.search((app.outdir / f"{page}.html").read_text(encoding='utf-8'), re.DOTALL).group(0)

    data_regression.check(data)
