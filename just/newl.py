def read(fname):
    with open(fname) as f:
        return f.read().split("\n")


def iread(fname):
    with open(fname) as f:
        for line in f:
            yield line.strip()


def write(obj, fname):
    with open(fname, "w") as f:
        f.write("\n".join(obj))
