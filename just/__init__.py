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
from just.path_ import glob
from just.requests_ import get
from just.requests_ import post
from just.dir import mkdir
from just.log import log


__project__ = "just"
__version__ = "0.5.49"

EXT_TO_MODULE = {
    "html": txt,
    "py": txt,
    "txt": txt,
    "newl": newl,
    "json": json,
    "jsonl": json,
    "yaml": yaml,
    "yml": yaml,
    "csv": csv,
    "tsv": csv,
    "pickle": pickle,
    "pkl": pickle,
}


def reader(fname, no_exist, read_func_name, fallback_type):
    fname = make_path(fname)
    if not os.path.isfile(fname) and no_exist is not None:
        return no_exist
    ext = fname.split(".")[-1] if "." in fname[-6:] else "txt"
    if ext not in EXT_TO_MODULE and fallback_type == "RAISE":
        raise TypeError("just does not yet cover '{}'".format(ext))
    reader_module = EXT_TO_MODULE.get(ext, None) or EXT_TO_MODULE[fallback_type]
    read_fn = getattr(reader_module, read_func_name)
    return read_fn(fname)


def read(fname, no_exist=None, fallback_type="RAISE"):
    return reader(fname, no_exist, "read", fallback_type)


def multi_read(star_path, no_exist=None, fallback_type="RAISE"):
    return {x: read(x, no_exist, fallback_type) for x in glob(star_path)}


def writer(obj, fname, mkdir_no_exist, skip_if_exist, write_func_name):
    fname = make_path(fname)
    if skip_if_exist and os.path.isfile(fname):  # pragma: no cover
        return False
    if mkdir_no_exist:
        dname = os.path.dirname(fname)
        if dname not in set([".", "..", ""]):
            mkdir(dname)
    ext = fname.split(".")[-1] if "." in fname[-6:] else "txt"
    writer_module = EXT_TO_MODULE[ext]
    write_fn = getattr(writer_module, write_func_name)
    return write_fn(obj, fname)


def write(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    return writer(obj, fname, mkdir_no_exist, skip_if_exist, "write")

# only supported for JSON Lines so far.


def append(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    return writer(obj, fname, mkdir_no_exist, skip_if_exist, "append")


def multi_write(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    if not isinstance(fname, list) or not isinstance(obj, list):  # pragma: no cover
        raise NotImplementedError("Only list of fnames + list of objects supported.")
    return [write(o, fn, mkdir_no_exist, skip_if_exist)
            for o, fn in zip(obj, fname)]


def iread(fname, no_exist=None, fallback_type="RAISE"):
    return reader(fname, no_exist, "iread", fallback_type)


def iwrite(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    return writer(obj, fname, mkdir_no_exist, skip_if_exist, "iwrite")


def remove(fname, no_exist=None):
    fname = make_path(fname)
    if not os.path.isfile(fname) and no_exist is not None:
        return False
    os.remove(fname)
    return True


def rename(fname, extension, no_exist=None):
    fname = make_path(fname)
    if not os.path.isfile(fname) and no_exist is not None:
        return False
    os.rename(fname, fname + "." + extension)
    return True
