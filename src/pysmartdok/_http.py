import logging
from typing import Callable, Optional

import requests

logger = logging.getLogger(__name__)


class _HttpClient:
    """Base class for resource subclients.

    Holds a shared mutable `headers` dict whose Authorization entry is
    refreshed in place when the parent ApiClient re-authenticates. On a 401
    response, `_request` calls the optional `reauth` callback once and retries
    with the refreshed headers.
    """

    def __init__(
        self,
        api_url: str,
        headers: dict,
        reauth: Optional[Callable[[], None]] = None,
    ):
        self.api_url = api_url
        self.headers = headers
        self._reauth = reauth

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        response = requests.request(method, url, headers=self.headers, **kwargs)
        if response.status_code == 401 and self._reauth is not None:
            logger.info("Got 401 from %s; re-authenticating and retrying once", url)
            self._reauth()
            response = requests.request(method, url, headers=self.headers, **kwargs)
        return response
