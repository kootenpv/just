## just

[![Build Status](https://travis-ci.org/kootenpv/just.svg?branch=master)](https://travis-ci.org/kootenpv/just)
[![PyPI](https://img.shields.io/pypi/v/just.svg?style=flat-square)](https://pypi.python.org/pypi/just/)
[![PyPI](https://img.shields.io/pypi/pyversions/just.svg?style=flat-square)](https://pypi.python.org/pypi/just/)

### Intro

`just.read` a file like:

```python
txt = just.read("myfile.txt")
json = just.read("myfile.json")
yaml = just.read("myfile.yaml")
csv = just.read("myfile.csv")
pkl = just.read("myfile.pkl")
```

`just.write` a file like:

```python
just.write(txt, "myfile.txt")
just.write(json, "myfile.json")
just.write(yaml, "myfile.yaml")
just.write(csv, "myfile.csv")
just.write(pkl, "myfile.pkl")
```

### Install

Code is under CI, works on python 2 and 3:

    pip install just

### TODO

- Implement a way to handle paths, e.g.:

    just.read("base", "path", "myfile.txt")

- Or implement a way to set a base bath for a project globally

- Add streaming reader/writers, `just.iread` and `just.iwrite`

- csv should probably use the smart builtin csv Sniffer

- Add optional backends like urllib, requests, bs4, lxml, pandas

- Add requests.get/post to return "aware" content, e.g. json/txt
