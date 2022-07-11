import logging
import os
import platform as sysinfo

import requests

import staxapp
from staxapp.exceptions import ApiException

logging.getLogger().setLevel(os.environ.get("LOG_LEVEL", logging.INFO))


class Config:
    """
    Insert doco here
    """

    STAX_REGION = os.getenv("STAX_REGION", "au1.staxapp.cloud")
    API_VERSION = "20190206"

    api_config = dict()
    access_key = None
    secret_key = None
    auth_class = None
    _initialized = False
    base_url = None
    _hostname = f"api.{STAX_REGION}"
    org_id = None
    auth = None
    expiration = None
    load_live_schema = True

    platform = sysinfo.platform()
    python_version = sysinfo.python_version()
    sdk_version = staxapp.__version__

    def set_config(self):
        self.base_url = f"https://{self.hostname}/{self.API_VERSION}"
        config_url = f"{self.api_base_url()}/public/config"
        config_response = requests.get(config_url)
        try:
            config_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"{config_response.status_code}: {config_response.json()}")
            raise ApiException(
                str(e), config_response, detail=" Could not load API config."
            )

        self.api_config = config_response.json()

    def init(self, config=None, hostname=None):
        if hostname is not None and self.hostname is None:
            self.hostname = hostname
        if self._initialized:
            return

        if not config:
            self.set_config()

        self._initialized = True

    def api_base_url(self):
        return self.base_url

    @classmethod
    def GetDefaultConfig(cls):
        config = Config()
        return config

    def branch(cls):
        return os.getenv("STAX_BRANCH", "master")

    @classmethod
    def schema_url(cls):
        return f"https://{cls.hostname}/{cls.API_VERSION}/public/api-document"

    @classmethod
    def get_auth_class(cls):
        if cls.auth_class is None:
            from staxapp.auth import ApiTokenAuth

            cls.auth_class = ApiTokenAuth
        return cls.auth_class
