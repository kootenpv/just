""" You can kind of see this as the scope of `just` when you 'import just'
The following functions become available:
just.__project__
just.__version__
just.run
just.print_version
"""

import os
import glob
import just.txt as txt
import just.json_ as json
import just.yaml_ as yaml
import just.csv_ as csv
import just.pickle_ as pickle
from just.dir import mkdir

__project__ = "just"
__version__ = "0.1.15"

EXT_TO_MODULE = {
    "html": txt,
    "txt": txt,
    "json": json,
    "yaml": yaml,
    "csv": csv,
    "pickle": pickle,
    "pkl": pickle,
}


def join_path(*args):
    return os.path.expanduser(os.path.join(*args))


def _read(fname, no_exist):
    if not os.path.isfile(fname):
        if no_exist != "Throw":
            return no_exist
    ext = fname.split(".")[-1] if "." in fname[-5:] else "txt"
    return EXT_TO_MODULE[ext].read(fname)


def multi_read(star_path, no_exist="Throw"):
    return [_read(x, no_exist) for x in glob.glob(os.path.expanduser(star_path))]


def read(*fnargs, **kwargs):
    no_exist = kwargs.get("no_exist", "Throw")
    fname = fnargs[-1]
    if isinstance(fname, list):
        return [_read(join_path(*fnargs[:-1] + (fn,)), no_exist=no_exist) for fn in fname]
    else:
        return _read(join_path(*fnargs), no_exist=no_exist)


def _write(obj, fname, mkdir_no_exist, skip_if_exist):
    if skip_if_exist and os.path.isfile(fname):
        return False
    if mkdir_no_exist:
        dname = os.path.dirname(fname)
        if dname not in set([".", "..", ""]):
            mkdir(dname)
    ext = fname.split(".")[-1]
    if ext in EXT_TO_MODULE:
        return EXT_TO_MODULE[ext].write(obj, fname)


def write(obj, *fnargs, **kwargs):
    mkdir_no_exist = kwargs.get("mkdir_no_exist", True)
    skip_if_exist = kwargs.get("skip_if_exist", False)
    fname = fnargs[-1]
    if isinstance(fname, list):
        if not isinstance(obj, list):
            raise NotImplementedError("Only list of fnames + list of objects supported.")
        else:
            return [_write(o,
                           join_path(*fnargs[:-1] + (fn,)),
                           mkdir_no_exist=mkdir_no_exist,
                           skip_if_exist=skip_if_exist)
                    for o, fn in zip(obj, fname)]
    else:
        return _write(obj,
                      join_path(*fnargs),
                      mkdir_no_exist=mkdir_no_exist,
                      skip_if_exist=skip_if_exist)


def iread(fname):
    ext = fname.split(".")[-1] if "." in fname[-5:] else "txt"
    return EXT_TO_MODULE[ext].iread(fname)
