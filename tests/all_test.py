""" Our tests are defined in here """
import os
from operator import eq
import just
import pytest

TEST_FNAME = "testobj"


def get_result(m, extension, inp):
    fname = TEST_FNAME + "." + extension
    try:
        m.write(inp, fname)
        read_result = m.read(fname)
    finally:
        os.remove(fname)
    return read_result


@pytest.mark.parametrize("m, extension, inp, expected, compare", [
    (just, "txt", "{}", "{}", eq),
    (just.txt, "txt", "{}", "{}", eq),
    (just.txt, "txt", "None", "None", eq),
    (just.txt, "txt", "", "", eq),
    (just.json, "json", {}, {}, eq),
    (just.json, "json", None, None, eq),
    (just.json, "json", "", "", eq),
    (just.yaml, "yaml", {}, {}, eq),
    (just.yaml, "yaml", None, None, eq),
    (just.yaml, "yaml", "", "", eq),
    (just.pickle, "pkl", {}, {}, eq),
    (just.pickle, "pkl", None, None, eq),
    (just.pickle, "pkl", "", "", eq),
    (just.csv, "csv", [["1", "a"], ["2", "b"]], [["1", "a"], ["2", "b"]], eq),
])
def test_compare(m, extension, inp, expected, compare):
    assert compare(get_result(m, extension, inp), expected)


def test_multi_read():
    obj = ["a", "b"]
    fnames = ["a.txt", "b.txt"]
    just.write(obj, fnames)
    try:
        assert just.read(fnames) == obj
    finally:
        for fname in fnames:
            os.remove(fname)
