import json
import logging

import requests

from stax.config import Config


class Api:
    _requests_auth = None

    @classmethod
    def _auth(cls):
        if not cls._requests_auth:
            cls._requests_auth = Config.auth().requests_auth(
                Config.access_key, Config.secret_key
            )
        return cls._requests_auth

    @classmethod
    def get(cls, url_frag, params={}, **kwargs):
        url_frag = url_frag.replace(f"/{Config.API_VERSION}", "")
        url = f"{Config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.get(url, auth=cls._auth(), params=params, **kwargs)
        # logging.debug(f"GET: {response.text}")
        response.raise_for_status()
        return response.json()

    @classmethod
    def post(cls, url_frag, payload={}, **kwargs):
        url_frag = url_frag.replace(f"/{Config.API_VERSION}", "")
        url = f"{Config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.post(url, json=payload, auth=cls._auth(), **kwargs)
        # logging.debug(f"POST: {response.text}")
        if response.status_code == 400:
            logging.error(f"400: {response.json()}")
        else:
            response.raise_for_status()
        return response.json()

    @classmethod
    def put(cls, url_frag, payload={}, **kwargs):
        url_frag = url_frag.replace(f"/{Config.API_VERSION}", "")
        url = f"{Config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.put(url, json=payload, auth=cls._auth(), **kwargs)
        if response.status_code == 400:
            logging.error(f"400: {response.json()}")
        else:
            response.raise_for_status()
        return response.json()

    @classmethod
    def delete(cls, url_frag, params={}, **kwargs):
        url_frag = url_frag.replace(f"/{Config.API_VERSION}", "")
        url = f"{Config.api_base_url()}/{url_frag.lstrip('/')}"

        response = requests.delete(url, auth=cls._auth(), params=params, **kwargs)
        response.raise_for_status()
        return response.json()
