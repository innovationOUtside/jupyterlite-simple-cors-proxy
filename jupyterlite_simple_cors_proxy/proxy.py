# File: simple_cors_proxy/proxy.py
from urllib.parse import urlencode, quote
import requests
import requests_cache
import io
import platform
from typing import Optional, Union

PLATFORM = platform.system().lower()

class CorsProxy:
    """CORS Proxy with optional caching support."""
    
    def __init__(self, use_cache: bool = False, **cache_kwargs):
        """
        Initialize the CORS proxy.
        
        Args:
            use_cache: Whether to enable request caching
            **cache_kwargs: Arguments passed to requests_cache.CachedSession
                          (e.g., cache_name, backend, expire_after)
        """
        if use_cache:
            # Set some sensible defaults if not provided
            if 'cache_name' not in cache_kwargs:
                cache_kwargs['cache_name'] = 'cors_proxy_cache'
            if 'expire_after' not in cache_kwargs:
                cache_kwargs['expire_after'] = 3600  # 1 hour default
            self.session = requests_cache.CachedSession(**cache_kwargs)
        else:
            self.session = requests

    def xurl(self, url: str, params: Optional[dict] = None, force: bool = False) -> str:
        """Generate a proxied URL."""
        if PLATFORM == "emscripten" or force:
            if params:
                url = f"{url}?{urlencode(params)}"
            url = f"https://corsproxy.io/{quote(url)}"
        return url

    def furl(self, url: str, params: Optional[dict] = None, force: bool = False) -> io.BytesIO:
        """Return file like object after calling the proxied URL."""
        r = self.cors_proxy_get(url, params, force)
        return io.BytesIO(r.content)

    def cors_proxy_get(self, url: str, params: Optional[dict] = None, force: bool = False) -> requests.Response:
        """
        CORS proxy for GET resources with requests-like response.
        
        Args:
            url: The URL to fetch
            params: Query parameters to include
            force: Force using the proxy even on non-emscripten platforms
            
        Returns:
            A requests response object.
        """
        proxy_url = self.xurl(url, params, force)
        return self.session.get(proxy_url)

    def robust_get_request(self, url: str, params: Optional[dict] = None) -> requests.Response:
        """
        Try to make a simple request else fall back to a proxy.
        """
        try:
            r = self.session.get(url, params=params)
        except:
            r = self.cors_proxy_get(url, params=params)
        return r

# Create default instance
_default_proxy = CorsProxy()

# Legacy function-based interface
xurl = _default_proxy.xurl
furl = _default_proxy.furl
cors_proxy_get = _default_proxy.cors_proxy_get
robust_get_request = _default_proxy.robust_get_request

# Convenience function to create a cached proxy
def create_cached_proxy(**cache_kwargs):
    """Create a new CorsProxy instance with caching enabled."""
    return CorsProxy(use_cache=True, **cache_kwargs)