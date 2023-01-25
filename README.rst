.. image:: https://smutch.github.io/snakedoc/_images/snakedoc-logo.svg
   :width: 30%
   :align: center
   :class: no-scaled-link

A `Sphinx`_ extension for `Snakemake`_ workflows.

|tests badge| |coverage badge| |pre-commit badge|
|git3moji badge| |black badge| |isort badge|

`Snakemake`_ workflows can be complicated and difficult to follow, especially
for new users. Having good documentation explaining what each rule is doing,
what assumptions are being made, and what parts can be configured are important
for understandable and reusable workflows. `Snakedoc`_ aims to help with this
by:

1. encouraging developers to write contextual and useful docstrings, inline
   with their rules; and
2. providing a way to automatically scrape those docstrings and present them in
   Sphinx documentation where they can be further augmented as needed.


Where to go from here
---------------------

* See the `installation <https://smutch.github.io/snakedoc/installation.html>`_
  page how to install Snakedoc.
* To get started, check out the `guide
  <https://smutch.github.io/snakedoc/guide.html>`_.



.. _Sphinx: https://www.sphinx-doc.org/
.. _Snakemake: https://snakemake.readthedocs.io/
.. _Snakedoc: https://smutch.github.io/snakedoc/

.. |tests badge| image:: https://github.com/smutch/snakedoc/actions/workflows/tests.yaml/badge.svg
   :target: https://github.com/smutch/snakedoc/actions/workflows/tests.yaml
   :alt: tests status

.. |coverage badge| image:: https://codecov.io/gh/smutch/snakedoc/branch/main/graph/badge.svg?token=JJNMO2HMG6
   :target: https://codecov.io/gh/smutch/snakedoc
   :alt: coverage statistic

.. |pre-commit badge| image:: https://results.pre-commit.ci/badge/github/smutch/snakedoc/main.svg
   :target: https://results.pre-commit.ci/latest/github/smutch/snakedoc/main
   :alt: pre-commit.ci status

.. |git3moji badge| image:: https://img.shields.io/badge/git3moji-%E2%9A%A1%EF%B8%8F%F0%9F%90%9B%F0%9F%93%BA%F0%9F%91%AE%F0%9F%94%A4-fffad8.svg?style=flat-square
   :target: https://robinpokorny.github.io/git3moji/
   :alt: git3moji

.. |black badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Formatted with black

.. |isort badge| image:: https://img.shields.io/badge/imports-isort-ef8336.svg
   :target: https://github.com/pycqa/isort
   :alt: Imports formatted with isort
