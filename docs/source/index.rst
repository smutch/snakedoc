:hero: A Sphinx extension for generating Snakemake workflow documentation.

Snakedoc
========


Installation
------------

.. warning::
   Not actually true yet!

Snakedoc can be installed via `pip <https://pip.pypa.io/en/stable/>`_::

    pip install -U snakedoc

or `conda <https://docs.conda.io/en/latest/>`_::

    conda install -c conda-forge snakedoc


Motivation
----------

Large Snakemake workflows can quickly become complex and opaque to users (i.e. non-authors trying to use and modify the workflow). Snakedoc is an attempt to alleviate this issue by:

1. Encouraging developers to write contextual and **useful** docstrings inline with their rules, in a well defined format.
2. Providing a way to automatically scrape that information and present it in Sphinx documentation where it can be further augmented if needed.

|

.. toctree::
   :hidden:
   :caption: Snakedoc
