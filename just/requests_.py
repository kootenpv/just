import time
import requests
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
import diskcache
from just.dir import mkdir
from just.read_write import write

session = None

caches = {}
timers = {}
sessions = {}


def _retry(method, max_retries, delay_base, raw, caching, sleep_time, kwargs):
    from requests import RequestException

    tries = 0
    url = kwargs["url"]
    domain_name = url.split("/")[2].split("?")[0].replace("www.", "")

    use_cache, *cache_key = caching
    cache_key = tuple(cache_key)

    if use_cache:

        if domain_name not in caches:
            base = mkdir("~/.just_requests/")
            caches[domain_name] = diskcache.Cache(base + domain_name)

        if cache_key in caches[domain_name]:
            return caches[domain_name][cache_key]

    else:
        if caches.get(domain_name, {}).get(cache_key):
            del caches[domain_name][cache_key]

    if "timeout" not in kwargs:
        kwargs["timeout"] = delay_base

    if domain_name not in sessions:
        sessions[domain_name] = requests.Session()

    # e.g. GET or POST
    request_fn = getattr(sessions[domain_name], method)

    if sleep_time and domain_name in timers:
        # 1200 - 1201 + 3
        diff = timers[domain_name] - time.time() + sleep_time

        if diff > 0:
            time.sleep(diff)

    # retrying
    while tries < max_retries:
        try:
            r = request_fn(**kwargs)
            if r.status_code > 399:
                r = None
            break
        except RequestException as e:
            tries += 1
            print("just.requests_", kwargs["url"], "attempt", tries, str(e))
            if tries == max_retries:
                r = ""
                break
            time.sleep(delay_base ** tries)

    timers[domain_name] = time.time()

    # result handling
    if r is None or r == "":
        pass
    elif raw:
        r = r.content
    elif "application/json" in r.headers['Content-Type']:
        r = r.json()
    else:
        r = r.text

    if use_cache:
        caches[domain_name][cache_key] = r

    return r


def get(
    url,
    params=None,
    max_retries=1,
    delay_base=3,
    raw=False,
    use_cache=False,
    sleep_time=None,
    session_name=None,
    fname=None,
    **kwargs,
):
    caching = (use_cache, url, params)

    kwargs['url'] = url
    if params is not None:
        kwargs['params'] = params

    result = _retry("get", max_retries, delay_base, raw, caching, sleep_time, kwargs)

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
    sleep_time=None,
    session_name=None,
    fname=None,
    **kwargs,
):
    caching = (use_cache, url, params, data, json)

    kwargs['url'] = url
    if params is not None:
        kwargs['params'] = params
    if data is not None:
        kwargs["data"] = data
    if json is not None:
        kwargs["json"] = json

    result = _retry("post", max_retries, delay_base, raw, caching, sleep_time, kwargs)

    if fname is not None:
        write(result, fname)

    return result


def save_session(name, session):
    if any(["Session" in x.__name__ for x in session.__class__.__mro__]):
        try:
            print("trf")
            session.transfer_driver_cookies_to_session()
        except Exception as e:
            print("ERR", e)
        session = {"headers": session.headers, "cookies": dict_from_cookiejar(session.cookies)}
    write(session, f"~/.just_sessions/" + name + ".json")
