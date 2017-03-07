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
        for line in f:
            yield json.loads(line)


def iwrite(obj, fn):
    with open(fn, "w") as f:
        for chunk in obj:
            f.write(json.dumps(chunk) + "\n")
