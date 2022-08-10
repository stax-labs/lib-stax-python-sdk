import json

import requests

from staxapp.config import Config
from staxapp.exceptions import ApiException


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

    @staticmethod
    def handle_api_response(response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ApiException(str(e), response)

    @classmethod
    def get(cls, url_frag, params={}, config=None, **kwargs):
        config = cls.get_config(config)
        url_frag = url_frag.replace(f"/{config.API_VERSION}", "")
        url = f"{config.api_base_url()}/{url_frag.lstrip('/')}"
        response = requests.get(
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

        response = requests.post(
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

        response = requests.put(
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

        response = requests.delete(
            url,
            auth=config._auth(),
            params=params,
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()
