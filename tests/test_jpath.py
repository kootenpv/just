from just import jpath


def test_jpath():
    dc = {"a": 1}
    assert jpath(dc, "a") == 1


def test_jpath_list():
    dc = {"a": [{"b": 1}, {"b": 2}]}
    assert jpath(dc, "a.[*].b") == [1, 2]
