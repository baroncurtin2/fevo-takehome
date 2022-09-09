import logging
from dataclasses import dataclass, field, InitVar

import requests
from requests.exceptions import HTTPError

from .cache import CachingStrategy, STRATEGIES


class RestClientError(Exception):
    """Wrapper around HTTP Errors"""

    pass


@dataclass
class RestClient:
    cache_type: InitVar[str] = "dict"
    base_url: str = ""
    api_key: str | None = None
    headers: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    session: requests.Session = field(default_factory=requests.Session)
    cache_strategy: CachingStrategy = field(init=False)

    def __post_init__(self, cache_type: str = "dict"):
        self.cache_strategy = STRATEGIES.get(cache_type)()

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        response = self.session.request(
            method,
            f"{self.base_url}/{url}",
            headers=self.headers,
            params=self.params,
            **kwargs,
        )

        try:
            response.raise_for_status()
        except HTTPError as e:
            logging.error(response.content)
            raise RestClientError(e) from e
        return response

    def get(self, url: str, **kwargs) -> requests.Response:
        return self._request("GET", url, **kwargs)

    def update_headers(self, new_headers: dict) -> None:
        self.headers.update(new_headers)

    def update_params(self, new_params: dict) -> None:
        self.params.update(new_params)
