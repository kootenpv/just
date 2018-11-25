from jsonpath_rw import parse


def json_extract(dc, expr):
    res = parse(expr).find(dc)
    if len(res) == 1:
        res = res[0].value
    else:
        res = [x.value for x in res]
    return res
