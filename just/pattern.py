import re
from dateutil.parser import parse


def parse_specials(special_str):
    return [x.split(":") if ":" in x else (x, None) for x in special_str.split(",")]


def convert_str(format_str, names):
    r = ""
    on = False
    specials = []
    types = []
    tmp = ""
    lenm = len(format_str)
    last = -1
    captured_names = []
    for i, x in enumerate(format_str):
        if x == "}":
            on = False
            tp = str
            capture = True
            fw = False
            for name, value in parse_specials(tmp):
                if name == "cast":
                    tp = eval(value)
                elif name == "drop":
                    capture = False
                elif name == "fw":
                    fw = True
                elif name == "":
                    pass
                else:
                    raise ValueError("unknown")
            if fw:
                pat = ".{4}"
            elif i + 1 == lenm:
                pat = ".+"
            else:
                pat = f"[^{format_str[i+1]}]+"
            capture_name = names.pop(0) if names is not None else len(captured_names)
            if capture:
                types.append(tp)
                pat = f"({pat})"
                captured_names.append(capture_name)
            r += pat
            tmp = ""
            last = len(r)
        elif x == "{":
            on = True
        else:
            if not on:
                r += re.escape(x)
            else:
                tmp += x
    r = r[:last]
    return r, types, captured_names


class Pattern:
    def __init__(self, format_str, names=None):
        self.format_str = format_str
        self.pattern, self.types, self.names = convert_str(format_str, names)
        if len(self.types) == 1:
            self.type = self.types[0]
            self.find = self.finder_one
        else:
            self.find = self.finder_multi
        self.r = re.compile(self.pattern)

    def finder_one(self, line):
        res = self.r.search(line)
        if not res:
            return None
        return self.type(res.groups()[0])

    def finder_multi(self, line):
        res = self.r.search(line)
        if not res:
            return None
        return [tp(x) for tp, x in zip(self.types, res.groups())]
