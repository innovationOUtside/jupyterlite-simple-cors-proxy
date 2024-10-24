# jupyterlite-simple-cors-proxy
Simple CORS proxy for making http requests from JupyterLite

## Installation

```bash
pip install jupyterlite-simple-cors-proxy
```

## Usage

```python
from simple_cors_proxy import cors_proxy

# Make a request
url = "https://api.example.com/data"
params = {"key": "value"}
response = cors_proxy(url, params)

# Use like requests
print(response.text)
data = response.json()
raw = response.content
```

## Features

- Simple CORS proxy wrapper
- Requests-like response object
- Support for URL parameters
- JSON parsing
