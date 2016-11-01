
def read(fn, delim=None):
    if delim is None:
        delim = ","
    with open(fn) as f:
        return [x.rstrip('\n').split(delim) for x in f]


def write(obj, fn, delim=None):
    if delim is None:
        delim = ","
    with open(fn, "w") as f:
        f.write("\n".join([delim.join(x) for x in obj]))
