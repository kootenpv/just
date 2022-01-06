import os
import time
import warnings
import hashlib
from collections import defaultdict

from just.dir import mkdir
from just.path_ import exists, glob, make_path, remove, rename
from just.read_write import write, read

session = None
PER_FOLDER = 3000

caches = {}
timers = {}
sessions = {}
last_cache_fname = {}

obj_counts = defaultdict(int)


def get_domain(url):
    return url.split("/")[2].split("?")[0].replace("www.", "")


def delete_from_cache(url, cache_key=None, compression=".gz"):
    domain_name = get_domain(url)
    if cache_key is not None:
        fname = get_cache_file_name_str(domain_name, cache_key, compression)
        parts = fname.split()
        parts[-2] = "*"
        fname = glob("/".join(parts))[0]
    else:
        fname = last_cache_fname[domain_name]
    remove(fname)
    return fname


def update_obj_count(domain, dir_name, obj_type):
    if obj_type not in obj_counts:
        dir_name = make_path(dir_name)
        try:
            existing_partitions = glob(make_path(dir_name) + "/*")
            if existing_partitions:
                latest_folder = max(existing_partitions)
                base = int(latest_folder.split("/")[-1]) * PER_FOLDER
                count = base + len(os.listdir(latest_folder))
            else:
                count = 0
        except FileNotFoundError:
            count = 0
        obj_counts[(domain, obj_type)] = count
    return obj_counts[(domain, obj_type)]


def get_cache_file_name(domain, request_info, compression=".gz"):
    from preconvert.output import json

    key = json.dumps(request_info)
    m = hashlib.md5()
    m.update(key.encode("utf8"))
    md5 = m.hexdigest()
    dir_name, fname = md5[:3], md5[3:]
    if not compression:
        compression = ""
    return f"~/.just_requests/{domain}/{dir_name}/{fname}.json{compression}"


def get_obj_type(cache_key):
    if isinstance(cache_key, bool):
        obj_type, fname = "", ""
    else:
        if "/" in cache_key:
            obj_type, fname = cache_key.split("/")
        else:
            obj_type, fname = "", cache_key
        if obj_type:
            obj_type = "/" + obj_type
    return obj_type, fname


def get_cache_file_name_str(domain, cache_key, compression=".gz"):
    obj_type, fname = get_obj_type(cache_key)
    initial_part = f"~/.just_requests/{domain}{obj_type}"
    partition = update_obj_count(domain, initial_part, obj_type) // PER_FOLDER
    if not compression:
        compression = ""
    return f"{initial_part}/{partition}/{fname}.json{compression}"


def from_cache(url, cache_key, paths_only=False, compression=".gz"):
    domain = get_domain(url)
    obj_type, fname = get_obj_type(cache_key)
    initial_part = f"~/.just_requests/{domain}{obj_type}"
    partition = "*"
    paths = glob(f"{initial_part}/{partition}/{fname}.json{compression}")
    if paths_only:
        return paths
    return [read(x)["resp"] for x in paths]


def _retry(
    method,
    max_retries,
    delay_base,
    raw,
    caching,
    cache_compression,
    sleep_time,
    reuse_session,
    kwargs,
):
    import requests
    from requests import RequestException, Session
    from requests.utils import cookiejar_from_dict

    tries = 0
    url = kwargs["url"]
    domain_name = get_domain(url)

    use_cache, *request_info = caching

    if isinstance(use_cache, bool):
        cache_file_name = get_cache_file_name(domain_name, request_info, cache_compression)
    else:
        if isinstance(use_cache, int):
            use_cache = str(use_cache)
        cache_file_name = get_cache_file_name_str(domain_name, use_cache, cache_compression)

    if isinstance(use_cache, str):
        old_file_name = get_cache_file_name(domain_name, request_info, cache_compression)
        if exists(old_file_name):
            mkdir("/".join(cache_file_name.split("/")[:-1]))
            print("renaming existing to", cache_file_name)
            rename(old_file_name, cache_file_name)

    if exists(cache_file_name):
        if not use_cache:
            remove(cache_file_name)
        else:
            last_cache_fname[domain_name] = cache_file_name
            return read(cache_file_name)["resp"]

    if "timeout" not in kwargs:
        kwargs["timeout"] = delay_base

    cookies = kwargs.get("cookies")
    if isinstance(cookies, dict):
        kwargs["cookies"] = cookiejar_from_dict(cookies)

    if reuse_session:
        if domain_name not in sessions:
            sessions[domain_name] = Session()

        # e.g. GET or POST
        request_fn = getattr(sessions[domain_name], method)
    else:
        request_fn = getattr(requests, method)

    if sleep_time and domain_name in timers:
        # 1200 - 1201 + 3
        diff = timers[domain_name] - time.time() + sleep_time

        if diff > 0:
            time.sleep(diff)

    # retrying
    err = False
    r = None
    while tries < max_retries:
        try:
            r = request_fn(**kwargs)
            if r.status_code > 399:
                err = None
            break
        except RequestException as e:
            print("just.requests_", kwargs["url"], "attempt", tries, str(e))
            if tries == max_retries:
                err = ""
                r = None
                break
            tries += 1
            time.sleep(delay_base ** tries)

    timers[domain_name] = time.time()

    # result handling
    if err is None or err == "":
        text = r.text[:500] if r is not None else ""
        if len(text) == 500:
            text += "..."
        code = r.status_code if r is not None else None
        print("ERR", code, url, text)
        tmp = err
        try:
            err = r.json()
        except:
            try:
                err = r.text
            except:
                err = ""
        r = tmp
    elif raw:
        r = r.content
    elif r is None:
        pass
    elif r is not None and "application/json" in r.headers["Content-Type"]:
        r = r.json()
    else:
        r = r.text

    if use_cache and r is not None:
        result = {"resp": r, "request_info": request_info, "response_ts": time.time()}
        if err:
            result["error"] = err
        write(result, cache_file_name)
        obj_type, _ = get_obj_type(use_cache)
        obj_counts[(domain_name, obj_type)] += 1

    return r


def get(
    url,
    params=None,
    max_retries=1,
    delay_base=3,
    raw=False,
    use_cache=False,
    cache_compression=".gz",
    sleep_time=None,
    fname=None,
    reuse_session=True,
    **kwargs,
):
    caching = (use_cache, url, params)

    kwargs["url"] = url
    if params is not None:
        kwargs["params"] = params

    result = _retry(
        "get",
        max_retries,
        delay_base,
        raw,
        caching,
        cache_compression,
        sleep_time,
        reuse_session,
        kwargs,
    )

    if fname is not None:
        write(result, fname)

    return result


get.from_cache = from_cache


def warn_cache():
    warnings.warn(
        "This attribute is deprecated as boolean, it still works but advised to make a str key",
        DeprecationWarning,
        stacklevel=2,
    )


def post(
    url,
    params=None,
    data=None,
    max_retries=5,
    raw=False,
    json=None,
    delay_base=3,
    use_cache=False,
    cache_compression=".gz",
    sleep_time=None,
    fname=None,
    reuse_session=True,
    **kwargs,
):
    if isinstance(use_cache, bool):
        warn_cache()

    caching = (use_cache, url, params, data, json)

    kwargs["url"] = url
    if params is not None:
        kwargs["params"] = params
    if data is not None:
        kwargs["data"] = data
    if json is not None:
        kwargs["json"] = json

    result = _retry(
        "post",
        max_retries,
        delay_base,
        raw,
        caching,
        cache_compression,
        sleep_time,
        reuse_session,
        kwargs,
    )

    if fname is not None:
        write(result, fname)

    return result


post.from_cache = from_cache


def get_tree(*args, **kwargs):
    import lxml.html

    return lxml.html.fromstring(get(*args, **kwargs))


def save_session(name, session):
    from requests.utils import dict_from_cookiejar

    if any(["Session" in x.__name__ for x in session.__class__.__mro__]):
        try:
            print("trf")
            session.transfer_driver_cookies_to_session()
        except Exception as e:
            print("ERR", e)
        session = {"headers": session.headers, "cookies": dict_from_cookiejar(session.cookies)}
    write(session, f"~/.just_sessions/" + name + ".json")
