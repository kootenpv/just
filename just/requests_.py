import time
import hashlib
from just.dir import mkdir
from just.path_ import exists, remove
from just.read_write import write, read

session = None

caches = {}
timers = {}
sessions = {}


def get_cache_file_name(domain, request_info, compression=".gz"):
    from preconvert.output import json

    key = json.dumps(request_info)
    m = hashlib.md5()
    m.update(key.encode("utf8"))
    md5 = m.hexdigest()
    dir_name, f_name = md5[:3], md5[3:]
    if not compression:
        compression = ""
    return f"~/.just_requests/{domain}/{dir_name}/{f_name}.json{compression}"


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
    domain_name = url.split("/")[2].split("?")[0].replace("www.", "")

    use_cache, *cache_key = caching

    cache_file_name = get_cache_file_name(domain_name, cache_key, cache_compression)

    if exists(cache_file_name):
        if not use_cache:
            remove(cache_file_name)
        else:
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
        result = {"resp": r, "request_info": cache_key}
        if err:
            result["error"] = err
        write(result, cache_file_name)

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
