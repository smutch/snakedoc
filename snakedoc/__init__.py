def setup(app, *args, **kwargs):
    from .smk import setup

    return setup(app, *args, **kwargs)
