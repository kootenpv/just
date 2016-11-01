import csv

def read(fn, delimiter=None, quotechar=None):
    if delimiter is None:
        delimiter = ','
    if quotechar is None:
        quotechar = '"'
    with open(fn, 'rb') as f:
        return [row for row in csv.reader(f, delimiter=delimiter,
                                          quotechar=quotechar)]


def write(obj, fn, delimiter=None, quotechar=None):
    if delimiter is None:
        delimiter = ','
    if quotechar is None:
        quotechar = '"'
    with open(fn, "wb") as f:
        writer_ = csv.writer(f, delimiter=delimiter,
                             quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
        writer_.writerows(obj)
