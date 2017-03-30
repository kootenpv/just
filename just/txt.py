def read(fname):
    with open(fname) as f:
        return f.read()


def iread(fname):
    with open(fname) as f:
        for line in f:
            yield line.rstrip("\n")


def write(obj, fname):
    with open(fname, "w") as f:
        f.write(obj)
