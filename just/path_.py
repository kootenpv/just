import inspect
import os
import glob2

__cached_just_path = None


def glob(path):
    return glob2.glob(make_path(path))


def get_just_env_path():
    return os.environ.get("JUST_PATH")


def find_just_path(base=None, max_depth=5):
    if base is None:
        base = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
    for depth in range(max_depth):
        prefix = "../" * depth
        just_file = os.path.join(base, prefix, ".just")
        if os.path.isfile(just_file):
            print("just_file", os.path.abspath(os.path.dirname(just_file)))
            return os.path.abspath(os.path.dirname(just_file))
    return None


def get_likely_path():
    # try:
    # main_path = os.path.abspath(sys.modules['__main__'].__file__)
    # except AttributeError:
    main_path = os.path.realpath('__file__')
    return os.path.dirname(main_path)


def get_just_path():
    global __cached_just_path
    if __cached_just_path is not None:
        return __cached_just_path
    just_path = get_just_env_path()
    just_path = just_path if just_path is not None else find_just_path()
    just_path = just_path if just_path is not None else find_just_path(".")
    just_path = just_path if just_path is not None else get_likely_path()
    __cached_just_path = just_path
    return just_path


def make_path(filename):
    just_path = get_just_path()
    filename = filename.replace("file://", "")
    return os.path.join(just_path, os.path.expanduser(filename))
