from requests import RequestException
from retrying import retry

import json
import requests


def fetch(request_fn, kwargs):

    try:
        r = request_fn(**kwargs)
        if "application/json" in r.headers['Content-Type']:
            return r.json()
        return r.text
    except RequestException as _:
        return ""


@retry(stop_max_attempt_number=3, wait_fixed=2000)  # 2000 = 2 seconds.
def get(url, params=None, **kwargs):
    kwargs['url'] = url
    kwargs['params'] = json.dumps(params) if params else ''
    result = fetch(requests.get, kwargs)
    return result


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def post(url, params=None, data=None, **kwargs):
    kwargs['url'] = url
    kwargs['params'] = json.dumps(params) if params else ''
    kwargs['data'] = json.dumps(data) if data else ''
    result = fetch(requests.post, kwargs)
    return result
