""" You can kind of see this as the scope of `just` when you 'import just'
The following functions become available:
just.__project__
just.__version__
just.run
just.print_version
"""

import os
import gzip
import shutil
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
from just.jpath import json_extract

__project__ = "just"
__version__ = "0.6.92"

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


def reader(fname, no_exist, read_func_name, unknown_type, ignore_exceptions):
    fname = make_path(fname)
    if not os.path.isfile(fname) and no_exist is not None:
        return no_exist
    gzname = False
    if fname.endswith(".gz"):
        gzname = fname
        fname = fname[:-3]
    ext = fname.split(".")[-1] if "." in fname[-6:] else "txt"
    if ext not in EXT_TO_MODULE and unknown_type == "RAISE":
        raise TypeError("just does not yet cover '{}'".format(ext))
    reader_module = EXT_TO_MODULE.get(ext, None) or EXT_TO_MODULE[unknown_type]
    read_fn = getattr(reader_module, read_func_name)
    if ignore_exceptions is not None:
        try:
            if gzname:
                # actually returns a file handler >.<
                with gzip.GzipFile(gzname, "rb") as f:
                    return read_fn(f)
            else:
                return read_fn(fname)
        except ignore_exceptions:
            return None
    else:
        if gzname:
            # actually returns a file handler >.<
            with gzip.GzipFile(gzname, "rb") as f:
                return read_fn(f)
        else:
            return read_fn(fname)


def read(fname, no_exist=None, unknown_type="RAISE", ignore_exceptions=None):
    return reader(fname, no_exist, "read", unknown_type, ignore_exceptions)


def multi_read(star_path, no_exist=None, unknown_type="RAISE", ignore_exceptions=None):
    return {x: read(x, no_exist, unknown_type, ignore_exceptions) for x in glob(star_path)}


def writer(obj, fname, mkdir_no_exist, skip_if_exist, write_func_name):
    fname = make_path(fname)
    if skip_if_exist and os.path.isfile(fname):  # pragma: no cover
        return False
    if mkdir_no_exist:
        dname = os.path.dirname(fname)
        if dname not in set([".", "..", ""]):
            mkdir(dname)
    gzname = False
    if fname.endswith(".gz"):
        gzname = fname
        fname = fname[:-3]
    ext = fname.split(".")[-1] if "." in fname[-6:] else "txt"
    writer_module = EXT_TO_MODULE[ext]
    write_fn = getattr(writer_module, write_func_name)
    if gzname:
        # actually returns a file handler >.<
        with gzip.GzipFile(gzname, "w") as f:
            return write_fn(obj, f)
    else:
        return write_fn(obj, fname)


def write(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    return writer(obj, fname, mkdir_no_exist, skip_if_exist, "write")


# only supported for JSON Lines so far.


def append(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    return writer(obj, fname, mkdir_no_exist, skip_if_exist, "append")


def multi_write(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    if not isinstance(fname, list) or not isinstance(obj, list):  # pragma: no cover
        raise NotImplementedError("Only list of fnames + list of objects supported.")
    return [write(o, fn, mkdir_no_exist, skip_if_exist) for o, fn in zip(obj, fname)]


def iread(fname, no_exist=None, unknown_type="RAISE", ignore_exceptions=None):
    return reader(fname, no_exist, "iread", unknown_type, ignore_exceptions)


def iwrite(obj, fname, mkdir_no_exist=True, skip_if_exist=False):
    return writer(obj, fname, mkdir_no_exist, skip_if_exist, "iwrite")


def remove(file_path, no_exist=False, allow_recursive=False):
    if isinstance(file_path, (tuple, list)):
        file_path = os.path.join(*file_path)
    if "*" in file_path:
        if not allow_recursive:
            raise IOError("Cannot remove wildcard unless allow_recursive=True")
        paths = glob(file_path)
        for fn in sorted(paths, key=lambda x: -len(x)):
            os.remove(fn)
        return bool(paths)
    file_path = make_path(file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    if os.path.isdir(file_path):
        if allow_recursive:
            shutil.rmtree(file_path)
            return True
        else:
            raise IOError("Cannot remove directory unless allow_recursive=True")
    # if there is a default value, return that if no file/dir found when attempting to remove
    if no_exist is not None:
        return no_exist
    raise IOError("File '{}' does not exist.".format(file_path))


def exists(fname):
    return os.path.isfile(make_path(fname))


def rename(fname, extension, no_exist=None):
    fname = make_path(fname)
    if not os.path.isfile(fname) and no_exist is not None:
        return False
    os.rename(fname, fname + "." + extension)
    return True


def jpath(fname_or_dc, jsonpath_expression):
    if isinstance(fname_or_dc, str):
        fname_or_dc = read(fname_or_dc)
    return json_extract(fname_or_dc, jsonpath_expression)
