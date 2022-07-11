import json

import requests

from staxapp.config import Config
from staxapp.exceptions import ApiException


class Api:
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
    def get(cls, url_frag, auth, config, params={}, **kwargs):
        url_frag = url_frag.replace(f"/{config.API_VERSION}", "")
        url = f"{config.api_base_url()}/{url_frag.lstrip('/')}"
        response = requests.get(
            url,
            auth=auth,
            params=params,
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()

    @classmethod
    def post(cls, url_frag, auth, config, payload={}, **kwargs):
        url_frag = url_frag.replace(f"/{config.API_VERSION}", "")
        url = f"{config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.post(
            url,
            json=payload,
            auth=auth,
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()

    @classmethod
    def put(cls, url_frag, auth, config, payload={}, **kwargs):
        url_frag = url_frag.replace(f"/{config.API_VERSION}", "")
        url = f"{config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.put(
            url,
            json=payload,
            auth=auth,
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()

    @classmethod
    def delete(cls, url_frag, auth, config, params={}, **kwargs):
        url_frag = url_frag.replace(f"/{config.API_VERSION}", "")
        url = f"{config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.delete(
            url,
            auth=auth,
            params=params,
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()
