""" You can kind of see this as the scope of `just` when you 'import just'
The following functions become available:
just.__project__
just.__version__
just.run
just.print_version
"""

import just.txt as txt
import just.json_ as json
import just.yaml_ as yaml
import just.csv_ as csv
import just.pickle_ as pickle

__project__ = "just"
__version__ = "0.0.9"

EXT_TO_MODULE = {
    "txt": txt,
    "json": json,
    "yaml": yaml,
    "csv": csv,
    "pickle": pickle,
    "pkl": pickle,
}


def _read(fname):
    ext = fname.split(".")[-1] if "." in fname else "txt"
    return EXT_TO_MODULE[ext].read(fname)


def read(fname):
    if isinstance(fname, list):
        return [_read(fn) for fn in fname]
    else:
        return _read(fname)


def _write(obj, fname):
    ext = fname.split(".")[-1]
    if ext in EXT_TO_MODULE:
        return EXT_TO_MODULE[ext].write(obj, fname)


def write(obj, fname):
    if isinstance(fname, list):
        if not isinstance(obj, list):
            raise NotImplementedError
        else:
            return [_write(o, fn) for o, fn in zip(obj, fname)]
    else:
        return _write(obj, fname)
