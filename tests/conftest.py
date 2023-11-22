import sys
from pathlib import Path

import pytest
import sphinx
from bs4 import BeautifulSoup
from sphinx.application import Sphinx

pytest_plugins = 'sphinx.testing.fixtures'

# Exclude 'roots' dirs for pytest test collector
collect_ignore = ['roots']


@pytest.fixture(scope='session')
def rootdir():
    if sphinx.version_info[0] < 7 or sys.version_info < (3, 9):
        return sphinx.testing.path.path(__file__).parent.abspath() / 'roots'
    return (Path(__file__).parent / 'roots').resolve()


def build_and_blend(app: Sphinx, file: str = "index.html") -> str:
    app.builder.build_all()
    html = app.outdir / file

    assert html.exists()
    with open(html, "r") as fp:
        soup = BeautifulSoup(fp, "html.parser")
    return soup


def get_rule(rule_name: str, soup: BeautifulSoup) -> str:
    return " ".join(
        list(filter(lambda dl: dl.find("dt", id=f"rule-{rule_name}"), soup.find_all("dl")).__next__().stripped_strings)
    )
