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


Autodoc
-------

.. smk:autodoc:: tests/workflow/Snakefile


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
