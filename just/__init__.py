""" You can kind of see this as the scope of `just` when you 'import just'
The following functions become available:
just.__project__
just.__version__
just.run
just.print_version
"""

import os

import just.txt as txt
import just.json_ as json
import just.newl as newl
import just.yaml_ as yaml
import just.csv_ as csv
import just.pickle_ as pickle
from just.path_ import make_path
from just.requests import get
from just.requests import post
from just.dir import mkdir

from glob2 import glob

__project__ = "just"
__version__ = "0.4.34"

EXT_TO_MODULE = {
    "html": txt,
    "py": txt,
    "txt": txt,
    "newl": newl,
    "json": json,
    "yaml": yaml,
    "yml": yaml,
    "csv": csv,
    "tsv": csv,
    "pickle": pickle,
    "pkl": pickle,
}


class Throw():
    """ This class exists to not confuse modules, while still allowing None """
    pass


def reader(fname, no_exist, read_func_name):
    fname = make_path(fname)
    if not os.path.isfile(fname) and not isinstance(no_exist, Throw):
        return no_exist
    ext = fname.split(".")[-1] if "." in fname[-5:] else "txt"
    reader_module = EXT_TO_MODULE[ext]
    read_fn = getattr(reader_module, read_func_name)
    return read_fn(fname)


def read(fname, no_exist=Throw):
    return reader(fname, no_exist, "read")


def multi_read(star_path, no_exist=Throw):
    return {x: read(x, no_exist) for x in glob(os.path.expanduser(star_path))}


def write(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    fname = make_path(fname)
    if skip_if_exist and os.path.isfile(fname):  # pragma: no cover
        return False
    if mkdir_no_exist:
        dname = os.path.dirname(fname)
        if dname not in set([".", "..", ""]):
            mkdir(dname)
    ext = fname.split(".")[-1]
    if ext in EXT_TO_MODULE:
        return EXT_TO_MODULE[ext].write(obj, fname)


def multi_write(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    if not isinstance(fname, list) or not isinstance(obj, list):  # pragma: no cover
        raise NotImplementedError("Only list of fnames + list of objects supported.")
    return [write(o, fn, mkdir_no_exist, skip_if_exist)
            for o, fn in zip(obj, fname)]


def iread(fname, no_exist=Throw):
    return reader(fname, no_exist, "iread")


def remove(fname, no_exist=Throw):
    fname = make_path(fname)
    if not os.path.isfile(fname) and not isinstance(no_exist, Throw):
        return False
    os.remove(fname)
    return True
