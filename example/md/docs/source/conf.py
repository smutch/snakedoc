# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from pathlib import Path

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Markdown Example'
copyright = '2023, Simon Mutch'
author = 'Simon Mutch'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["snakedoc", "myst_parser"]

smk_linkcode_mapping = (str(Path(__file__).parents[2]), "https://github.com/smutch/snakedoc/blob/master/example/md")

napoleon_custom_sections = [("Params", "params_style")]
napoleon_use_admonition_for_notes = True

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
