.. Snakedoc documentation master file, created by
   sphinx-quickstart on Thu May 12 11:56:15 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Snakedoc's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Hello world!

.. smk:rule:: basic
   :source: abc

   This is a basic rule docstring.

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


.. smk:autodoc:: ../test/workflow/Snakefile



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`smk-rule`
* :ref:`search`
