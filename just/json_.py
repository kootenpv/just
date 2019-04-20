import warnings
import gzip

try:
    import ujson as json
except ImportError:
    import json


def read(fn):
    if isinstance(fn, gzip.GzipFile):
        return json.load(fn)
    if fn.endswith(".jsonl"):
        warnings.warn("Reading streaming format at once.")
        return list(iread(fn))
    with open(fn) as f:
        return json.load(f)


def append(obj, fn):
    if isinstance(fn, gzip.GzipFile):
        raise TypeError("Cannot append to gzip")
    with open(fn, "a+") as f:
        f.write(json.dumps(obj) + "\n")


def write(obj, fn):
    if isinstance(fn, gzip.GzipFile):
        json.dump(obj, fn)
    else:
        with open(fn, "w") as f:
            json.dump(obj, f, indent=4)


def iread(fn):
    if isinstance(fn, gzip.GzipFile):
        raise TypeError("Cannot iteratively read gzip")
    with open(fn) as f:
        for i, line in enumerate(f):
            try:
                yield json.loads(line)
            except json.decoder.JSONDecodeError as e:
                msg = "JSON-L parsing error in line number {} in the jsonl file".format(i)
                raise json.decoder.JSONDecodeError(msg, line, e.pos)


def iwrite(obj, fn):
    if isinstance(fn, gzip.GzipFile):
        raise TypeError("Cannot iteratively write gzip")
    with open(fn, "w") as f:
        for chunk in obj:
            f.write(json.dumps(chunk) + "\n")
