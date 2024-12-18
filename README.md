# jupyterlite-simple-cors-proxy
Simple CORS proxy for making http requests from JupyterLite

## Installation

```bash
pip install jupyterlite-simple-cors-proxy
```

## Usage

```python
from jupyterlite_simple_cors_proxy.proxy import cors_proxy_get, robust_get_request

# Make a request
url = "https://api.example.com/data"
params = {"key": "value"}
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
