import time
import requests
import diskcache
from just.dir import mkdir

session = None

caches = {}
timers = {}
sessions = {}


def _retry(method, max_retries, delay_base, raw, cache_key, sleep_time, kwargs):
    from requests import RequestException

    tries = 0
    url = kwargs["url"]
    domain_name = url.split("/")[2].split("?")[0].replace("www.", "")

    if cache_key:

        if domain_name not in caches:
            base = mkdir("~/.just_requests/")
            caches[domain_name] = diskcache.Cache(base + domain_name)

        if cache_key in caches[domain_name]:
            return caches[domain_name][cache_key]

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

    if cache_key:
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
    **kwargs
):
    cache_key = (url, params) if use_cache else False

    global session
    if session is None:
        session = requests.Session()

    kwargs['url'] = url
    if params is not None:
        kwargs['params'] = params

    result = _retry("get", max_retries, delay_base, raw, cache_key, sleep_time, kwargs)

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
    **kwargs
):
    cache_key = (url, params, data, json) if use_cache else False

    kwargs['url'] = url
    if params is not None:
        kwargs['params'] = params
    if data is not None:
        kwargs["data"] = data
    if json is not None:
        kwargs["json"] = json

    result = _retry("post", max_retries, delay_base, raw, cache_key, sleep_time, kwargs)

    return result
