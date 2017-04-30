try:
    import ujson as json
except ImportError:
    import json


def read(fn):
    if fn.endswith(".jsonl"):
        raise TypeError("JSON Newline format can only be read by iread")
    with open(fn) as f:
        return json.load(f)


def append(obj, fn):
    with open(fn, "a+") as f:
        f.write(json.dumps(obj) + "\n")


def write(obj, fn):
    with open(fn, "w") as f:
        json.dump(obj, f, indent=4)


def iread(fn):
    with open(fn) as f:
        for i, line in enumerate(f):
            try:
                yield json.loads(line)
            except json.decoder.JSONDecodeError as e:
                msg = "JSON-L parsing error in line number {} in the jsonl file".format(i)
                raise json.decoder.JSONDecodeError(msg, line, e.pos)


def iwrite(obj, fn):
    with open(fn, "w") as f:
        for chunk in obj:
            f.write(json.dumps(chunk) + "\n")
