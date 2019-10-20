import time
import json

session = None


def _retry(request_fn, max_retries, delay_base, raw, kwargs):
    from requests import RequestException

    tries = 0
    if 'headers' not in kwargs:
        kwargs["headers"] = {}
    if 'User-Agent' not in kwargs:
        kwargs["headers"]['User-Agent'] = 'Just Agent 1.0'
    while tries < max_retries:
        try:
            r = request_fn(timeout=delay_base, **kwargs)
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


def get(url, params=None, max_retries=1, delay_base=3, raw=False, **kwargs):
    import requests

    global session
    if session is None:
        session = requests.Session()

    kwargs['url'] = url
    kwargs['params'] = json.dumps(params) if params else ''
    result = _retry(session.get, max_retries, delay_base, raw, kwargs)
    return result


def post(url, params=None, data=None, max_retries=5, raw=False, delay_base=3, **kwargs):
    import requests

    global session
    if session is None:
        session = requests.Session()

    kwargs['url'] = url
    kwargs['params'] = json.dumps(params) if params else ''
    kwargs['data'] = json.dumps(data) if data else ''
    result = _retry(session.post, max_retries, delay_base, raw, kwargs)
    return result
