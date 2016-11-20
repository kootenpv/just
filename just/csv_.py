def iread(fn):
    import dsv
    for line in dsv.iread(fn):
        yield line


def read(fn):
    import dsv
    return dsv.read(fn)


def write(obj, fn):
    import dsv
    dsv.write(obj, fn)
