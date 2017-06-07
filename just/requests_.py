import time
import json


def retry(request_fn, max_retries, delay_base, kwargs):
    from requests import RequestException
    tries = 0
    if 'headers' not in kwargs:
        kwargs["headers"] = {}
    if 'User-Agent' not in kwargs:
        kwargs["headers"]['User-Agent'] = 'Just Agent 1.0'
    while tries < max_retries:
        try:
            r = request_fn(**kwargs)
            break
        except RequestException as e:
            tries += 1
            print("just.requests_", kwargs["url"], "attempt", tries, str(e))
            if tries == max_retries:
                return ""
            time.sleep(delay_base ** tries)
    if "application/json" in r.headers['Content-Type']:
        return r.json()
    return r.text


def get(url, params=None, max_retries=3, delay_base=3, **kwargs):
    import requests
    kwargs['url'] = url
    kwargs['params'] = json.dumps(params) if params else ''
    result = retry(requests.get, max_retries, delay_base, kwargs)
    return result


def post(url, params=None, data=None, max_retries=3, delay_base=3, **kwargs):
    import requests
    kwargs['url'] = url
    kwargs['params'] = json.dumps(params) if params else ''
    kwargs['data'] = json.dumps(data) if data else ''
    result = retry(requests.post, max_retries, delay_base, kwargs)
    return result
