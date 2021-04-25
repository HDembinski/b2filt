import pathlib

# we first assume you are developing
fn = pathlib.Path(__file__).parent.parent / "setup.cfg"
if fn.exists():
    import configparser

    cfg = configparser.ConfigParser()
    cfg.read(fn)
    version = cfg["metadata"]["version"]
else:
    import importlib_metadata

    version = importlib_metadata.distribution("b2filt").version
