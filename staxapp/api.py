"""
This module contains the http api handlers.
"""
import logging

import requests

from staxapp.config import Config, StaxAPIRetryConfig
from staxapp.exceptions import ApiException
from staxapp.retry import requests_retry_session


class Api:
    @classmethod
    def get_config(cls, config=None):
        if config is None:
            config = Config.GetDefaultConfig()
            config.init()
        return config

    @classmethod
    def _headers(cls, custom_headers) -> dict:
        headers = {
            **custom_headers,
            "User-Agent": f"platform/{Config.platform} python/{Config.python_version} staxapp/{Config.sdk_version}",
        }
        return headers

    @classmethod
    def request_session(cls, config: StaxAPIRetryConfig):
        """Requests retry session with backoff"""
        print(config.retry_methods)
        return requests_retry_session(
            retries=config.max_attempts,
            status_list=config.status_codes,
            allowed_methods=config.retry_methods,
            backoff_factor=config.backoff_factor,
        )

    @staticmethod
    def handle_api_response(response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # logging.debug(f"request retried {len(response.raw.retries.history)} times") ## Useful to prove working
            raise ApiException(str(e), response)

    @classmethod
    def get(cls, url_frag, params={}, config=None, **kwargs):
        config = cls.get_config(config)
        url_frag = url_frag.replace(f"/{config.API_VERSION}", "")
        url = f"{config.api_base_url()}/{url_frag.lstrip('/')}"

        response = cls.request_session(config.api_retry_config).get(
            url,
            auth=config._auth(),
            params=params,
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()

    @classmethod
    def post(cls, url_frag, payload={}, config=None, **kwargs):
        config = cls.get_config(config)
        url_frag = url_frag.replace(f"/{config.API_VERSION}", "")
        url = f"{config.api_base_url()}/{url_frag.lstrip('/')}"

        response = cls.request_session(config.api_retry_config).post(
            url,
            json=payload,
            auth=config._auth(),
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()

    @classmethod
    def put(cls, url_frag, payload={}, config=None, **kwargs):
        config = cls.get_config(config)
        url_frag = url_frag.replace(f"/{config.API_VERSION}", "")
        url = f"{config.api_base_url()}/{url_frag.lstrip('/')}"

        response = cls.request_session(config.api_retry_config).put(
            url,
            json=payload,
            auth=config._auth(),
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()

    @classmethod
    def delete(cls, url_frag, params={}, config=None, **kwargs):
        config = cls.get_config(config)
        url_frag = url_frag.replace(f"/{config.API_VERSION}", "")
        url = f"{config.api_base_url()}/{url_frag.lstrip('/')}"

        response = cls.request_session(config.api_retry_config).delete(
            url,
            auth=config._auth(),
            params=params,
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()
