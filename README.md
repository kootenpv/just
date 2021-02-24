## just

[![Build Status](https://travis-ci.org/kootenpv/just.svg?branch=master)](https://travis-ci.org/kootenpv/just)
[![Coverage Status](https://coveralls.io/repos/github/kootenpv/just/badge.svg?branch=master)](https://coveralls.io/github/kootenpv/just?branch=master)
[![PyPI](https://img.shields.io/pypi/v/just.svg?style=flat-square)](https://pypi.python.org/pypi/just/)
[![PyPI](https://img.shields.io/pypi/pyversions/just.svg?style=flat-square)](https://pypi.python.org/pypi/just/)

### Reasons

- You like the safety of `with` statements, just not in *your* code: let `just` take care of it.

- You like a computer to figure out how to load a file based on extension.

- You like sensible defaults for reading and writing.

### Intro

`just.read` a file like:

```python
some_txt = just.read("myfile.txt")
some_json = just.read("myfile.json")
some_yaml = just.read("myfile.yaml")
some_csv = just.read("myfile.csv")
some_pkl = just.read("myfile.pkl")
```

Multi-read is also possible:

```python
txts = just.multi_read("file*.txt")
jsons = just.multi_read("*.json")
```

**Multi-read is different as of 0.2.25, it now returns a dictionary instead of list; {"file.txt": "file_contents"}**

`just.write` a file like:

```python
just.write(some_txt, "myfile.txt")
just.write(some_json, "myfile.json")
just.write(some_yaml, "myfile.yaml")
just.write(some_csv, "myfile.csv")
just.write(some_pkl, "myfile.pkl")
```

### Compression

```python
just.write(some_json, "myfile.json.gz")
```

### More features

#### Return default structure when file does not exist:

```python
data = just.read("notexisting.txt", no_exist=[])
```

Like this you can still write a for loop, as you expect this file to be filled in a second run of the script.

#### Root directory

The logic of finding a root file is the following:

1. Environment variable `JUST_PATH`, if not set
2. Searching upwards to a `.just` file, if not found
3. The path where the script gets executed from

The rationale is that you can refer to 'data/images' from anywhere in your project. It will be relative to the "just path".

#### On write, creates paths when they don't exist

```python
data = just.write("data/txt/deep/1.png", mkdir_no_exist=True) # default
```

There's also an option to skip writing if the file exists, but this is not `True` by default.

```python
data = just.write("data/txt/deep/1.png", skip_if_exist=False) # default
```

#### Use glob

    from just import glob
    glob("**.txt")
    # lists filesnames

### Install

Code is under CI, tested to be working on python 2.7/3.3+:

    pip install just

### TODO

- Add streaming reader/writers, `just.iread` and `just.iwrite`

- Add optional backends like urllib, requests, bs4, lxml, pandas

- Add requests.get/post to return "aware" content, e.g. json/txt
