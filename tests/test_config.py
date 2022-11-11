import pytest
from sphinx.application import Sphinx

from .conftest import build_and_blend, get_rule


@pytest.mark.sphinx('html', testroot='docs')
def test_smk_configfile(app: Sphinx):
    soup = build_and_blend(app, "index.html")
    rule = get_rule("follows_basic", soup)

    assert "Config : omega_m – mass density" in rule
    assert "default: 0.27" in rule
    assert "galaxy.stellar_mass – the galaxy stellar mass" in rule
    assert "default: 9.1" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_smk_config(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("follows_basic", soup)

    assert "length – some random length" in rule
    assert "default: 15" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_sphinx_configfile(app: Sphinx):
    soup = build_and_blend(app, "config1.html")
    rule = get_rule("also_follows_basic", soup)

    assert "Config : omega_m – mass density" in rule
    assert "default: 0.27" in rule
    assert "galaxy.stellar_mass – the galaxy stellar mass" in rule
    assert "default: 9.1" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_sphinx_configdict(app: Sphinx):
    soup = build_and_blend(app, "config1.html")
    rule = get_rule("gen_random", soup)

    assert "conf1 – a config var" in rule
    assert "default: val1" in rule
