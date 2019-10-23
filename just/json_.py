import warnings


def read(fn, warn=False):
    from preconvert.output import json

    if not isinstance(fn, str):
        return json.load(fn)
    if fn.endswith(".jsonl"):
        if warn:
            warnings.warn("Reading streaming format at once.")
        return list(iread(fn))
    with open(fn) as f:
        return json.load(f)


def append(obj, fn):
    from preconvert.output import json

    if not isinstance(fn, str):
        raise TypeError("Cannot append to compression")
    with open(fn, "a+") as f:
        f.write(json.dumps(obj) + "\n")


def write(obj, fn):
    from preconvert.output import json

    if not isinstance(fn, str):
        fn.write(bytes(json.dumps(obj), encoding="utf8"))
    else:
        with open(fn, "w") as f:
            json.dump(obj, f, indent=4)


def iread(fn):
    from preconvert.output import json

    if not isinstance(fn, str):
        raise TypeError("Cannot iteratively read compressed file now")
    with open(fn) as f:
        for i, line in enumerate(f):
            try:
                yield json.loads(line)
            except Exception as e:
                msg = "JSON-L parsing error in line number {} in the jsonl file".format(i)
                raise Exception(msg, line)


def iwrite(obj, fn):
    from preconvert.output import json

    if not isinstance(fn, str):
        raise TypeError("Cannot iteratively write compressed")
    with open(fn, "w") as f:
        for chunk in obj:
            f.write(json.dumps(chunk) + "\n")
