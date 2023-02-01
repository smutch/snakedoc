Frequently Asked Questions
==========================

Can I use markdown instead of reStructuredText?
-----------------------------------------------

The answer yes... and no. You can write your Sphinx documentation files in
markdown instead of reStructuredText using the `MyST parser
<https://myst-parser.readthedocs.io/en/latest/>`_. See their documentation for
how to do this.

Unfortunately, MyST can't be used for docstrings (see the relevant `GitHub
issue <https://github.com/executablebooks/MyST-Parser/issues/228>`_) and we
have not yet assessed if we can easily circumvent this issue with Snakedoc.
However, Snakedoc is fully compatible with Google style docstrings (see the
first example of the :doc:`guide`), which is pretty nice and gets you most of
the way towards a more "markdowny" looking source.
