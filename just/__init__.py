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
import just.path_ as path
from just.requests import get
from just.requests import post
from just.dir import mkdir

__project__ = "just"
__version__ = "0.2.20"

EXT_TO_MODULE = {
    "html": txt,
    "txt": txt,
    "json": json,
    "yaml": yaml,
    "csv": csv,
    "pickle": pickle,
    "pkl": pickle,
}


def reader(fname, no_exist, read_func_name):
    fname = path.make_path(fname)
    if not os.path.isfile(fname) and no_exist != "Throw":
        return no_exist
    ext = fname.split(".")[-1] if "." in fname[-5:] else "txt"
    reader_module = EXT_TO_MODULE[ext]
    read_fn = getattr(reader_module, read_func_name)
    return read_fn(fname)


def read(fname, no_exist="Throw"):
    return reader(fname, no_exist, "read")


def multi_read(star_path, no_exist="Throw"):
    return [read(x, no_exist) for x in glob.glob(os.path.expanduser(star_path))]


def write(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    fname = path.make_path(fname)
    if skip_if_exist and os.path.isfile(fname):
        return False
    if mkdir_no_exist:
        dname = os.path.dirname(fname)
        if dname not in set([".", "..", ""]):
            mkdir(dname)
    ext = fname.split(".")[-1]
    if ext in EXT_TO_MODULE:
        return EXT_TO_MODULE[ext].write(obj, fname)


def multi_write(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    if not isinstance(fname, list) or not isinstance(obj, list):
        raise NotImplementedError("Only list of fnames + list of objects supported.")
    return [write(o, fn, mkdir_no_exist, skip_if_exist)
            for o, fn in zip(obj, fname)]


def iread(fname, no_exist="Throw"):
    return reader(fname, no_exist, "iread")


def remove(fname, no_exist="Throw"):
    fname = path.make_path(fname)
    if not os.path.isfile(fname) and no_exist != "Throw":
        return False
    os.remove(fname)
    return True
