from ._version import version as __version__


def setup(app, *args, **kwargs):
    from .smk import setup

    return setup(app, *args, **kwargs)
