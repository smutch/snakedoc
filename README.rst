Snakedoc
========

A `Sphinx`_ extension for `Snakemake`_ workflows.

**WIP!**

|tests badge| |pre-commit badge|

.. |tests badge| image:: https://github.com/smutch/snakedoc/actions/workflows/tests.yaml/badge.svg
   :target: https://github.com/smutch/snakedoc/actions/workflows/tests.yaml
   :alt: tests status

.. |pre-commit badge| image:: https://results.pre-commit.ci/badge/github/smutch/snakedoc/main.svg
   :target: https://results.pre-commit.ci/latest/github/smutch/snakedoc/main
   :alt: pre-commit.ci status


Take it for a spin
------------------

.. code-block:: shell

   git clone git@github.com:smutch/snakedoc.git
   cd snakedoc
   poetry install
   poetry shell
   cd example/docs
   make html
   open build/html/index.html


.. _`Sphinx`: https://www.sphinx-doc.org/
.. _`Snakemake`: https://snakemake.readthedocs.io/
