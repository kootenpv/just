import time
import json


def retry(request_fn, max_retries, delay_between_retries, kwargs):
    from requests import RequestException
    tries = 0
    while tries < max_retries:
        try:
            r = request_fn(**kwargs)
            break
        except RequestException as e:
            tries += 1
            print("just.requests_", kwargs["url"], "attempt", tries, str(e))
            if tries == max_retries:
                return ""
            time.sleep(delay_between_retries)
    if "application/json" in r.headers['Content-Type']:
        return r.json()
    else:
        return r.text


def get(url, params=None, max_retries=3, delay_between_retries=3, **kwargs):
    import requests
    kwargs['url'] = url
    kwargs['params'] = json.dumps(params) if params else ''
    result = retry(requests.get, max_retries, delay_between_retries, kwargs)
    return result


def post(url, params=None, data=None, max_retries=3, delay_between_retries=3, **kwargs):
    import requests
    kwargs['url'] = url
    kwargs['params'] = json.dumps(params) if params else ''
    kwargs['data'] = json.dumps(data) if data else ''
    result = retry(requests.post, max_retries, delay_between_retries, kwargs)
    return result
