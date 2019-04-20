import gzip


def read(fname):
    if isinstance(fname, gzip.GzipFile):
        return fname.read().decode()
    with open(fname) as f:
        return f.read()


def iread(fname):
    if isinstance(fname, gzip.GzipFile):
        raise TypeError("Cannot iteratively read gzip")
    with open(fname) as f:
        for line in f:
            yield line.rstrip("\n")


def write(obj, fname):
    if isinstance(fname, gzip.GzipFile):
        fname.write(obj)
    else:
        with open(fname, "w") as f:
            f.write(obj)
