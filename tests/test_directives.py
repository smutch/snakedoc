from pathlib import Path

import pytest
from sphinx.application import Sphinx

from snakedoc import smk

from .conftest import build_and_blend, get_rule


@pytest.mark.sphinx('html', testroot='docs')
def test_rule_directive(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("handwritten", soup)

    assert "Input : a.txt" in rule
    assert "Output : b.txt" in rule

    assert "Params : c – set c" in rule
    assert "d – set d" in rule

    assert "Conda : channels : - conda-forge" in rule[50:]

    assert "Resources : mem_mb – 2" in rule
    assert "Config : handwritten.a – A dummy config parameter used in this rule" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_checkpoint(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("hw_checkpoint", soup)

    assert "Input : a.txt" in rule
    assert "Output : b.txt" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_autodoc_directive(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("follows_basic", soup)

    assert "Config : omega_m – mass density" in rule
    assert "galaxy.stellar_mass – the galaxy stellar mass" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_autodoc_single_file(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("other", soup)

    assert "Input : an input file" in rule
    assert "Output : an output file" in rule


@pytest.mark.sphinx('html', testroot='conf')
def test_autodoc_config_overrides(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("dummy1", soup)

    assert "Config : omega_m – The matter density" in rule
    assert "default: 0.25" in rule


@pytest.mark.sphinx('html', testroot='conf', confoverrides={"smk_configfile": None})
def test_autodoc_config_fileopt(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("dummy1", soup)

    assert "Config : omega_m – The matter density" in rule
    assert "default: 0.25" in rule


@pytest.mark.sphinx(
    'html',
    testroot='conf',
    confoverrides={"smk_configfile": Path(__file__).absolute().parent / "roots/test-conf/workflow/config.yaml"},
)
def test_autodoc_config_absolute(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("dummy1", soup)

    assert "Config : omega_m – The matter density" in rule
    assert "default: 0.25" in rule


@pytest.mark.sphinx('html', testroot='conf_fail')
def test_autodoc_config_fail(app: Sphinx):
    with pytest.raises(smk.SmkAutoDocError):
        soup = build_and_blend(app)


@pytest.mark.sphinx('html', testroot='docs')
def test_autodoc_single_rule(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("other", soup)

    assert "Input : an input file" in rule
    assert "Output : an output file" in rule


@pytest.mark.sphinx('html', testroot='docs')
def test_autodoc_multiple_rules(app: Sphinx):
    soup = build_and_blend(app)
    rule = get_rule("other2", soup)
    assert "other2" in rule

    rule = get_rule("other3", soup)
    assert "other3" in rule
