# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

from pathlib import Path

# -- Project information -----------------------------------------------------

project = 'Snakedocs example'
copyright = '2022, Simon Mutch'
author = 'Simon Mutch'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["snakedoc"]


def smk_linkcode_resolve(domain, info):
    if len(info["source"]) == 0:
        return ""

    parts = info["source"].split(":")
    if len(parts) == 2:
        filename, lineno = parts
    elif len(parts) == 1:
        filename = parts[0]
        lineno = None
    try:
        filename = str(Path(filename).relative_to(Path.cwd().parent))
    except ValueError as err:
        raise ValueError(
            f"Rule lists {filename} as it's source, but this is not relative to {Path.cwd().parent}"
        ) from err

    return f"https://github.com/snakedoc/blob/master/example/{filename}{'#L'+lineno if lineno else ''}"


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
