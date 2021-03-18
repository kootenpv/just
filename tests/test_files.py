""" Our tests are defined in here """
import os
import sys
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
        just.remove(fname)
    return read_result


@pytest.mark.parametrize(
    "m, extension, inp, expected, compare",
    [
        (just, "txt", "{}", "{}", eq),
        (just.txt, "txt", "{}", "{}", eq),
        (just.txt, "txt", "None", "None", eq),
        (just.txt, "txt", "", "", eq),
        (just.newl, "newl", ["1", "2"], ["1", "2"], eq),
        (just.json, "json", {}, {}, eq),
        (just.json, "json", None, None, eq),
        (just.json, "json", "", "", eq),
        (just.yaml, "yaml", {}, {}, eq),
        (just.yaml, "yaml", None, None, eq),
        (just.yaml, "yaml", "", "", eq),
        (just.pickle, "pkl", {}, {}, eq),
        (just.pickle, "pkl", None, None, eq),
        (just.pickle, "pkl", "", "", eq),
    ],
)
def test_compare(m, extension, inp, expected, compare):
    assert compare(get_result(m, extension, inp), expected)


def test_multi_read():
    obj = ["a", "b"]
    fnames = ["a.txt", "b.txt"]
    just.multi_write(obj, fnames)
    try:
        for name, data in just.multi_read("*.txt"):
            assert fnames.index(name.split("/")[-1]) == obj.index(data)
    finally:
        for fname in fnames:
            os.remove(fname)


def test_newl_iread():
    fname = "testobj.newl"
    obj = ["1", "2"]
    just.write(obj, "testobj.newl")
    try:
        assert [x for x in just.iread(fname)] == [x for x in obj]
    finally:
        os.remove(fname)


def test_txt_iread():
    fname = "testobj.txt"
    obj = "1\n2\n3\n4\n5"
    just.write(obj, "testobj.txt")
    try:
        assert [x for x in just.iread(fname)] == [x for x in obj.split("\n")]
    finally:
        os.remove(fname)


def test_find_just_path():
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        just_file = os.path.join(base, ".just")
        with open(just_file, "w") as f:
            f.write("OK")
        assert isinstance(just.path_.find_just_path(), type("1"))
    finally:
        os.remove(just_file)


def test_txt_append():
    fname = "testobj.txt"
    obj = "bla"
    just.append(obj, "testobj.txt")
    try:
        assert [x for x in just.iread(fname)] == [obj]
        just.append(obj, "testobj.txt")
        assert [x for x in just.iread(fname)] == [obj, obj]
    finally:
        os.remove(fname)


def test_unsuccesful_read():
    assert just.read("A" * 100, 42) == 42


def test_unsuccesful_remove():
    assert just.remove("A" * 100, 42) == 42


def test_ls():
    assert just.ls(".")
