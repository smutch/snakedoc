.. snakedocs test input documentation master file, created by
   sphinx-quickstart on Tue May 17 16:07:25 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to snakedocs test input's documentation!
================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Handwritten docs
----------------

.. smk:rule:: handwritten

   This is a handwritten docstring.

   :input: a.txt
   :output: b.txt
   :param c: set ``c``
   :param d: set ``d``
   :conda:
     .. code-block:: yaml

         channels:
           - conda-forge
         dependencies:
           - pip:
             - test1
             - test2
   :resource mem_mb: 2
   :config handwritten.a: A dummy config parameter used in this rule

|

.. smk:checkpoint:: hw_checkpoint

   This is a handwritten docstring for a *checkpoint*.

   :input: a.txt
   :output: b.txt


Autodoc
-------

.. smk:autodoc:: workflow/Snakefile
   :configfile: workflow/config.yaml
   :config: this=is
            a=test
            length=15

:ref:`We can also autodoc single files. <single-file>`

... And single rules

.. smk:autodoc:: workflow/rules/others.smk other

... or a list of rules

.. smk:autodoc:: workflow/rules/others.smk other2 other3

We can also link between rules. See :smk:ref:`other2`.

This is a deliberate :smk:ref:`failed reference` for code coverage.

Indices and tables
==================

* :ref:`smk-rule`
* :ref:`search`
