
def read(fn):
    import pickle
    with open(fn, "rb") as f:
        return pickle.load(f)


def write(obj, fn):
    import pickle
    with open(fn, "wb") as f:
        pickle.dump(obj, f)
