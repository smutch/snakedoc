Snakedoc
========

A `Sphinx`_ extension for `Snakemake`_ workflows.

**WIP!**

|tests badge| |coverage badge| |pre-commit badge|

|git3moji badge| |black badge| |isort badge|

.. |tests badge| image:: https://github.com/smutch/snakedoc/actions/workflows/tests.yaml/badge.svg
   :target: https://github.com/smutch/snakedoc/actions/workflows/tests.yaml
   :alt: tests status

.. |coverage badge| image:: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/smutch/bbe05fc2211ebcc2ce35d446223426e0/raw/coverage-badge.json
   :target: https://github.com/smutch/snakedoc/actions/workflows/coverage.yaml
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

Take it for a spin
------------------

.. code-block:: shell

   git clone git@github.com:smutch/snakedoc.git
   cd snakedoc
   hatch shell
   cd example/docs
   make html
   open build/html/index.html


.. _`Sphinx`: https://www.sphinx-doc.org/
.. _`Snakemake`: https://snakemake.readthedocs.io/
