import os
import time
import json
import requests
import diskcache

session = None

caches = {}


def _retry(request_fn, max_retries, delay_base, raw, kwargs):
    from requests import RequestException

    tries = 0
    # if 'headers' not in kwargs:
    #     kwargs["headers"] = {}
    # if 'User-Agent' not in kwargs:
    #     kwargs["headers"]['User-Agent'] = 'Just Agent 1.0'
    if "timeout" not in kwargs:
        kwargs["timeout"] = delay_base
    while tries < max_retries:
        try:
            r = request_fn(**kwargs)
            if r.status_code > 399:
                return None
            break
        except RequestException as e:
            tries += 1
            print("just.requests_", kwargs["url"], "attempt", tries, str(e))
            if tries == max_retries:
                return ""
            time.sleep(delay_base ** tries)
    if raw:
        return r.content
    if "application/json" in r.headers['Content-Type']:
        return r.json()
    return r.text


def get(url, params=None, max_retries=1, delay_base=3, raw=False, cache_name=None, **kwargs):
    cache_key = (url, params)

    if cache_name is not None and cache_name not in caches:
        caches[cache_name] = diskcache.Cache(os.path.expanduser("~/.just_requests/" + cache_name))

    if cache_name is not None and cache_key in caches[cache_name]:
        return caches[cache_name][cache_key]

    global session
    if session is None:
        session = requests.Session()

    kwargs['url'] = url
    if params is not None:
        kwargs['params'] = params
    result = _retry(session.get, max_retries, delay_base, raw, kwargs)

    if cache_name is not None:
        caches[cache_name][cache_key] = result

    return result


def post(
    url,
    params=None,
    data=None,
    max_retries=5,
    raw=False,
    json=None,
    delay_base=3,
    cache_name=None,
    **kwargs
):
    cache_key = (url, params, data, json)
    if cache_name is not None and cache_name not in caches:
        caches[cache_name] = diskcache.Cache(os.path.expanduser("~/.just_requests/" + cache_name))

    if cache_name is not None and cache_key in caches[cache_name]:
        return caches[cache_name][cache_key]

    global session
    if session is None:
        session = requests.Session()

    kwargs['url'] = url
    if params is not None:
        kwargs['params'] = params
    if data is not None:
        kwargs["data"] = data
    if json is not None:
        kwargs["json"] = json

    result = _retry(session.post, max_retries, delay_base, raw, kwargs)

    if cache_name is not None:
        caches[cache_name][cache_key] = result

    return result
