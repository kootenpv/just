
def read(fn):
    import json
    with open(fn) as f:
        return json.load(f)


def write(obj, fn):
    import json
    with open(fn, "w") as f:
        json.dump(obj, f)
