import json

import requests

from staxapp.config import Config
from staxapp.exceptions import ApiException


class Api:
    _requests_auth = None

    @classmethod
    def _headers(cls, custom_headers) -> dict:
        headers = {
            **custom_headers,
            "User-Agent": json.dumps(
                {
                    "platform": Config.platform,
                    "python_version": Config.python_version,
                    "sdk_version": Config.sdk_version,
                }
            ),
        }
        return headers

    @classmethod
    def _auth(cls, **kwargs):
        if not cls._requests_auth:
            cls._requests_auth = Config.get_auth_class().requests_auth
        return cls._requests_auth(Config.access_key, Config.secret_key, **kwargs)

    @staticmethod
    def handle_api_response(response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ApiException(str(e), response)

    @classmethod
    def get(cls, url_frag, params={}, **kwargs):
        url_frag = url_frag.replace(f"/{Config.API_VERSION}", "")
        url = f"{Config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.get(
            url,
            auth=cls._auth(),
            params=params,
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()

    @classmethod
    def post(cls, url_frag, payload={}, **kwargs):
        url_frag = url_frag.replace(f"/{Config.API_VERSION}", "")
        url = f"{Config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.post(
            url,
            json=payload,
            auth=cls._auth(),
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()

    @classmethod
    def put(cls, url_frag, payload={}, **kwargs):
        url_frag = url_frag.replace(f"/{Config.API_VERSION}", "")
        url = f"{Config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.put(
            url,
            json=payload,
            auth=cls._auth(),
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()

    @classmethod
    def delete(cls, url_frag, params={}, **kwargs):
        url_frag = url_frag.replace(f"/{Config.API_VERSION}", "")
        url = f"{Config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.delete(
            url,
            auth=cls._auth(),
            params=params,
            headers=cls._headers(kwargs.get("headers", {})),
            **kwargs,
        )
        cls.handle_api_response(response)
        return response.json()
