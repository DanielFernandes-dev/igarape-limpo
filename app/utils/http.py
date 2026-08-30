import json
import urllib.error
import urllib.parse
import urllib.request

TIMEOUT = 15


class HttpError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.message = message
        self.status = status


def get(url, params=None, headers=None, timeout=TIMEOUT):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    return _request(url, method="GET", headers=headers, timeout=timeout)


def post(url, data=None, headers=None, form=None, timeout=TIMEOUT):
    if form:
        body = urllib.parse.urlencode(form).encode("utf-8")
        headers = dict(headers or {})
        headers.setdefault(
            "Content-Type", "application/x-www-form-urlencoded;charset=UTF-8"
        )
        return _request(url, method="POST", data=body, headers=headers, timeout=timeout)
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers = dict(headers or {})
        headers.setdefault("Content-Type", "application/json")
        return _request(url, method="POST", data=body, headers=headers, timeout=timeout)
    return _request(url, method="POST", headers=headers, timeout=timeout)


def _request(url, method="GET", data=None, headers=None, timeout=TIMEOUT):
    req = urllib.request.Request(url, data=data, method=method)
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            content_type = resp.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return resp.status, json.loads(raw.decode("utf-8"))
            return resp.status, raw.decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise HttpError(f"{method} {url} -> HTTP {exc.code}", status=exc.code)
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", None)
        raise HttpError(f"{method} {url} -> {reason}", status=None)
