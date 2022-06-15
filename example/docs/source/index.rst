Welcome to the Snakedocs example!
=================================

.. smk:autodoc:: ../workflow/Snakefile


Manually documented rule
------------------------

The following rule is manually documented in the docs source.


.. smk:rule:: handwritten

   This is a handwritten docstring.

   :input: A super-dooper result file
   :output: A swanky plot
   :param γ: The gradient of the line
   :config handwritten.length: A phony config parameter

|

.. smk:checkpoint:: handwritten_checkpoint

   Checkpoints are supported too.

   :input: Some data
   :output: A directory with an undetermined number of files

|

Indices and tables
==================

* :ref:`smk-rule`
