import re

import pytest
from sphinx.application import Sphinx

body_pattern = re.compile(r"<body>.*</body>", re.DOTALL)


@pytest.mark.sphinx('html', testroot='docs')
def test_build(data_regression, app: Sphinx):
    app.builder.build_all()
    assert (app.outdir / "index.html").exists()

    data = {}
    for page in ('index', 'smk-rule'):
        data[page] = body_pattern.search((app.outdir / f"{page}.html").read_text(encoding='utf-8'), re.DOTALL).group(0)

    data_regression.check(data)
