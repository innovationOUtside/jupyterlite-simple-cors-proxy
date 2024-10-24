# File: simple_cors_proxy/proxy.py
from urllib.parse import urlencode, quote
import requests


def cors_proxy_get(url, params=None):
    """
    CORS proxy for GET resources with requests-like response.

    Args:
        url (str): The URL to fetch
        params (dict, optional): Query parameters to include

    Returns:
        A requests response object.
    """
    if params:
        full_url = f"{url}?{urlencode(params)}"
    else:
        full_url = url

    proxy_url = f"https://corsproxy.io/?{quote(full_url)}"

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