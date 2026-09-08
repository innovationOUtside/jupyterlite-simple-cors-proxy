# jupyterlite-simple-cors-proxy
Simple CORS proxy wrapper for making http requests from JupyterLite. Uses https://corsproxy.io/

## Installation

```bash
pip install jupyterlite-simple-cors-proxy
```

## Usage

```python
from jupyterlite_simple_cors_proxy.proxy import cors_proxy_get, robust_get_request, furl, xurl

# Set up
url = "https://api.example.com/data"
# Optional params
params = {"key": "value"}

# Get a cross-origin proxied url
cross_origin_url = xurl(url) # xurl(url, params)

# Get a file like object
# (Make the request, then create a file like object
# from the response)
file_ob = furl(url) # furl(url, params)

# Make a request
response = cors_proxy_get(url, params)

# Use like requests
print(response.text)
data = response.json()
raw = response.content
```

The `robust_get_request()` will first try a simple request, then a proxied request: `robust_get_request(url, params)`

## Features

- Simple CORS proxy wrapper
- Requests response object
- Support for URL parameters

## Using an API key with a CORS proxy

Some proxies, such as `corsproxy.io`, support (or require) an API key, passed as `?key=abcd1234&url=...`. Pass it via the `api_key` argument on any of the helper functions:

```python
from jupyterlite_simple_cors_proxy.proxy import xurl, cors_proxy_get

cross_origin_url = xurl(url, api_key="abcd1234")
response = cors_proxy_get(url, params, api_key="abcd1234")
```

Or set a default `api_key` once when using the `CorsProxy` class:

```python
from jupyterlite_simple_cors_proxy.cacheproxy import CorsProxy

proxy = CorsProxy(api_key="abcd1234")
response = proxy.cors_proxy_get(url, params)  # api_key applied automatically
```

## `fastf1` cors proxy

A monkey patch for `fastf1` is provided as:

```python
import fast f1
from jupyterlite_simple_cors_proxy.fastf1_proxy import enable_cors_proxy

enable_cors_proxy(
#    domains=["api.formula1.com", "livetiming.formula1.com"],
#    debug=True,
#    proxy_url="https://corsproxy.io/",
)
```

## `CorsProxy` with cache facility

Via `claude.ai`, the package is now further enriched.

*Note that `pyodide` sqlite can't write to `/drive` so the cache path dir needs to be something like `/tmp` or a dir created on `/`.*

*I'm not convinced the following works in `pyodide` and `xeus-python` yet - `requests-cache` dependency issues etc. `requests-cache` has requirements `attrs`, `cattrs`,`platformdirs`, `url-normalize`.*

```python
from simple_cors_proxy.proxy import CorsProxy

# Create a cached proxy instance
proxy = CorsProxy(use_cache=True, expire_after=3600)  # Cache for 1 hour

# Optionally pass an api_key (and/or proxy) to use by default
proxy = CorsProxy(use_cache=True, expire_after=3600, api_key="abcd1234")

# Use furl directly from your proxy instance
file_like = proxy.furl('https://example.com/somefile.csv')

#----
import pandas as pd
from simple_cors_proxy.cacheproxy import CorsProxy

proxy = CorsProxy(use_cache=True)
file_like = proxy.furl('https://example.com/data.csv')
df = pd.read_csv(file_like)

#----

from simple_cors_proxy.proxy import create_cached_proxy

proxy = create_cached_proxy(cache_name='my_cache', expire_after=86400)  # Cache for 1 day
file_like = proxy.furl('https://example.com/somefile.csv')
```
