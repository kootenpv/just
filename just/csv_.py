
def read(fn):
    with open(fn) as f:
        return [x.rstrip('\n').split(",") for x in f]


def write(obj, fn):
    with open(fn, "w") as f:
        f.write("\n".join([",".join(x) for x in obj]))
