# File: simple_cors_proxy/proxy.py
from urllib.parse import urlencode, quote
import requests
import io

import platform
PLATFORM = platform.system().lower()

def xurl(url, params=None):
    if PLATFORM=="emscripten":
        if params:
            url = f"{url}?{urlencode(params)}"
        url = f"https://corsproxy.io/{quote(url)}"

    return url

def furl(url, params=None):
    """Return file like object."""
    r = cors_proxy_get(url, params)

    # Return a file-like object from the JSON string
    return io.BytesIO(r.content)


def cors_proxy_get(url, params=None):
    """
    CORS proxy for GET resources with requests-like response.

    Args:
        url (str): The URL to fetch
        params (dict, optional): Query parameters to include

    Returns:
        A requests response object.
    """
    proxy_url = xurl(url, params)

    # Do a simple requests get and
    # just pass through the entire response object
    return requests.get(proxy_url)

def robust_get_request(url, params=None):
    """
    Try to make a simple request else fall back to a proxy.
    """
    try:
        r = requests.get(url, params=params)
    except:
        r = cors_proxy_get(url, params=params)
    return r
