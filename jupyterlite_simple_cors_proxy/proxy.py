# File: simple_cors_proxy/proxy.py
from urllib.parse import urlencode, quote
import requests

class ProxyResponse:
    def __init__(self, content):
        self._content = content

    @property
    def text(self):
        return self._content

    def json(self):
        import json

        return json.loads(self._content)

    @property
    def content(self):
        return self._content.encode()


def cors_proxy(url, params=None):
    """
    CORS proxy for GET resources with requests-like response.

    Args:
        url (str): The URL to fetch
        params (dict, optional): Query parameters to include

    Returns:
        ProxyResponse: A response object with .text, .json(), and .content methods
    """
    if params:
        full_url = f"{url}?{urlencode(params)}"
    else:
        full_url = url

    proxy_url = f"https://corsproxy.io/?{quote(full_url)}"
    response = requests.get(proxy_url).content.decode().strip()
    return ProxyResponse(response)
