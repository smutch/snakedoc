Quickstart guide
================

.. |install Snakedoc| replace:: **install Snakedoc**
.. _install Snakedoc: installation.html

**If you haven't already, first** |install Snakedoc|_.


Add docstrings to your Snakemake workflow
-----------------------------------------

.. highlight:: text

The main feature of Snakedoc is to generate documentation for your Snakemake
workflow. To do this, you need to add docstrings to your rules. The docstrings
should be written in reStructuredText_ format, and should be placed in the
docstring attribute of the rule. For example [[#f1]_]::

    rule beast:
        """
        Run Beast2, either restarting from a state file or from scratch.

        :input alignment:         the aligned fasta file output from :smk:ref:`align`
        :input template:          the Beast 2 input XML file, templated with `feast <https://github.com/tgvaughan/feast>`_.
                                  If ``inherit`` is set in the config then the output of the :smk:ref:`onlinebeast` rule is used,
                                  otherwise the output of the :smk:ref:`dynamicbeast` rule is used.

        :output:                  the tree log, trace log, and statefile from Beast2

        :config inherit:          are we inheriting from a previous run?
        :config beast.dynamic:    the dynamic variables used to populate the feast template.
        :config beast.beast:      Beast2 command line arguments to pass (beyond the params, statefile and input)
        :config beast.threads:    the number of cores to run with (both locally or when submitting to a cluster)
        :config beast.resources:  the resources to request when submitting to a cluster

        :envmodules:              environment variables to load for the Spartan HPC system

        ..note::
            GPU acceleration is **not** requested by default. If you are running on a machine with a compatible GPU then
            please replace ``-beagle`` with ``-beagle_GPU`` in the ``beast.beast`` entry in your McCoy ``config.yaml`` file.
        """

        input:
            ...
        output:
            ...
        ...

.. [#f1] Taken from the `McCoy Phylodynamics Workflow
   <https://github.com/mccoy-devs/mccoy>`_.

If you are familiar with Python style rst-docstrings then you will feel right at home.

As recommended in Python, the basic layout of a docstring comprises of a short,
concise explanation of the purpose of the rule. This is then optionally
followed by a longer explanation, perhaps referencing relevant papers,
discussing potential issues and future improvements, etc.

Next comes a list of fields with a brief sentence or two indicating the logical
meaning and other useful information for each of the Snakemake directives and
their entries. Below is a list of reccognised directives that can be documented
using Snakedoc. Some can accept multiple, named values, as shown with the
``:input:`` and ``:config:`` fields in the example above. Others do not:

.. list-table:: Recognised Snakemake directives
   :header-rows: 1

   * - Name
     - Multiple values?
   * - input
     - ✅
   * - output
     - ✅
   * - param
     - ✅
   * - resource
     - ✅
   * - config
     - ✅
   * - log
     - ❎
   * - notebook
     - ❎
   * - shell
     - ❎
   * - script
     - ❎
   * - run
     - ❎
   * - wildcard_constraints
     - ❎
   * - threads
     - ❎
   * - priority
     - ❎
   * - retries
     - ❎
   * - benchmark
     - ❎
   * - group
     - ❎
   * - default_target
     - ❎


Finally, you may wish to include extra notes, caveats, etc. At the end of the docstring.

Note that you can include any valid reStructuredText_ and it will be marked up
accordingly (e.g. the ``..note::`` reStructuredText_ directives in the example above).


Set up Sphinx and Snakedoc
--------------------------


Generate your docs
------------------


What next?
----------

* Check out some examples


.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
