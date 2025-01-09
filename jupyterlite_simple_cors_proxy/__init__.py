# File: jupyterlite_simple_cors_proxy/__init__.py
from .proxy import cors_proxy_get, robust_get_request, xurl, furl

__version__ = "0.1.6"
__all__ = ["cors_proxy_get", "robust_get_request", "xurl", "furl"]
