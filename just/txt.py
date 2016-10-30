def read(fname):
    with open(fname) as f:
        return f.read()


def write(obj, fname):
    with open(fname, "w") as f:
        f.write(obj)
