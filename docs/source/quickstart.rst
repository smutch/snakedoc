Quickstart guide
================

.. |install Snakedoc| replace:: **install Snakedoc**
.. _install Snakedoc: installation.html

**If you haven't already, first** |install Snakedoc|_.


Add docstrings to your Snakemake workflow
-----------------------------------------

.. highlight:: text

The main feature of Snakedoc is the generation of documentation for your
Snakemake workflow. To do this, you need to add docstrings to the rules in your
Snakemake files. The docstrings should be written in reStructuredText_ format
and placed in triple quotes at the start of each rule, in exactly the same way
as you would document a Python function. For example [#f1]_::

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

If you are familiar with Python style rst-docstrings then you will feel right at home.

As recommended in normal Python code, the basic layout of a docstring comprises
of a short, concise explanation of the purpose of the rule. This is then
optionally followed by a longer explanation, perhaps referencing relevant
papers, discussing potential issues and future improvements, etc.

Next comes a list of fields with a brief sentence or two indicating the logical
meaning and other useful information for each of the Snakemake directives and
their entries. Below is a list of reccognised directives that can be documented
using Snakedoc. Some accept multiple, named values (c.f. the
``:input:`` and ``:config:`` fields in the example above). Others do not:

.. list-table:: Recognised Snakemake directives
   :header-rows: 1

   * - Name
     - # values
   * - benchmark
     - single
   * - config
     - multiple
   * - default_target
     - single
   * - group
     - single
   * - input
     - multiple
   * - log
     - single
   * - notebook
     - single
   * - output
     - multiple
   * - param
     - multiple
   * - priority
     - single
   * - resource
     - multiple
   * - retries
     - single
   * - run
     - single
   * - script
     - single
   * - shell
     - single
   * - threads
     - single
   * - wildcard_constraints
     - single


Finally, you may wish to include extra notes, caveats, etc. at the end of the docstring.
You can include any valid reStructuredText_ and it will be marked up
accordingly (e.g. the ``..note::`` reStructuredText_ directive in the example above).

For more basic examples, see the `example directory of the Snakedoc repo
<https://github.com/smutch/snakedoc/tree/main/example>`_. For an example of a
production pipeline fully documented with Snakedoc complete, check out the
`McCoy phylodynamics workflow <https://github.com/mccoy-devs/mccoy>`_.


Set up Sphinx and Snakedoc
--------------------------

.. highlight:: python

Begin by creating a standard Sphinx project using the `sphinx-quickstart <https://www.sphinx-doc.org/en/master/man/sphinx-quickstart.html>`_ tool. This will create a Sphinx configuration file called ``conf.py`` [#f2]_. To enable Snakedoc, simply add ``"snakedoc"`` to the extensions list::

    extensions = ["snakedoc"]

A useful feature of Snakedoc is to provide a link to the source code of each rule in the documentation. Since the head of this link will depend on the public location of your source code (Github, Bitbucket, Gitlab, private hosting, etc.) you need to provide a mapping between the full path to the source code on your local machine and the public link. This is set using the ``smk_linkcode_mapping`` config parameter, a 2-element tuple telling Snakedoc to replace all instances of the first element with the second.

For example, if your source code is located on your local machine in ``/home/username/workflow`` and your public Github repository is located at ``https://github.com/username/workflow``, then you could use something like the following::

    smk_linkcode_mapping = ("/home/username/workflow", "https://github.com/username/workflow/blob/master")

Since ``smk_linkcode_mapping`` is a Python tuple, you can use any valid Python code to make this work on any machine without hardcoding the path::

    from pathlib import Path
    smk_linkcode_mapping = (str(Path(__file__).parents[2]), "https://github.com/username/workflow/blob/master")


Generate your docs
------------------


What next?
----------

* Check out some examples


.. [#f1] Taken from the `McCoy Phylodynamics Workflow
   <https://github.com/mccoy-devs/mccoy>`_.

.. [#f2] https://www.sphinx-doc.org/en/master/usage/configuration.html#module-conf

.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
