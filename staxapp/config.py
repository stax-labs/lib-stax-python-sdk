import logging
import os
import platform as sysinfo
from typing import NamedTuple

import requests

import staxapp
from staxapp.exceptions import ApiException

logging.getLogger().setLevel(os.environ.get("LOG_LEVEL", logging.INFO))


class StaxAuthRetryConfig(NamedTuple):
    """
    Configuration options for the Stax API Auth retry
    max_attempts: int: number of attempts to make
    token_expiry_threshold: int: number of minutes before expiry to refresh
    """

    max_attempts = 5
    token_expiry_threshold = int(
        # Env Var for backwards compatability, deprecated since 1.3.0
        os.getenv("TOKEN_EXPIRY_THRESHOLD_IN_MINS", 1)
    )


class StaxAPIRetryConfig(NamedTuple):
    """
    Configuration options for the Stax API Auth retry

    max_attempts: int: number of attempts to make
    backoff_factor: float: exponential backoff factor
    status_codes: Tuple[int]: number of attempts to make
    retry_methods: Tuple[str]: http methods to perform retries on
    """

    max_attempts = 5
    backoff_factor = 1.0
    status_codes = (429, 500, 502, 504)
    retry_methods = ("GET", "PUT", "DELETE", "OPTIONS")


class Config:
    """
    Stax SDK Config
    """

    STAX_REGION = os.getenv("STAX_REGION", "au1.staxapp.cloud")
    API_VERSION = "20190206"

    cached_api_config = dict()
    api_config = dict()
    access_key = None
    secret_key = None
    auth_class = None
    auth = None
    _requests_auth = None
    _initialized = False
    base_url = None
    hostname = f"api.{STAX_REGION}"
    org_id = None
    expiration = None
    load_live_schema = True

    platform = sysinfo.platform()
    python_version = sysinfo.python_version()
    sdk_version = staxapp.__version__

    api_auth_retry_config = StaxAuthRetryConfig
    api_retry_config = StaxAPIRetryConfig

    def set_config(self):
        self.base_url = f"https://{self.hostname}/{self.API_VERSION}"
        config_url = f"{self.api_base_url()}/public/config"
        if config_url == self.cached_api_config.get("caching"):
            self.api_config = self.cached_api_config
        else:
            self.api_config = Config.get_api_config(config_url)

    @classmethod
    def get_api_config(cls, config_url):
        config_response = requests.get(config_url)
        try:
            config_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"{config_response.status_code}: {config_response.json()}")
            raise ApiException(
                str(e), config_response, detail=" Could not load API config."
            )
        cls.cached_api_config = config_response.json()
        cls.cached_api_config["caching"] = config_url
        return config_response.json()

    def __init__(
        self,
        hostname=None,
        access_key=None,
        secret_key=None,
        api_auth_retry_config=StaxAuthRetryConfig,
        api_retry_config=StaxAPIRetryConfig,
    ):
        if hostname is not None:
            self.hostname = hostname
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_auth_retry_config = api_auth_retry_config
        self.api_retry_config = api_retry_config

    def init(self):
        if self._initialized:
            return
        self.set_config()

        self._initialized = True

    def _auth(self, **kwargs):
        if not self._requests_auth:
            self._requests_auth = self.get_auth_class().requests_auth
        return self._requests_auth(self, **kwargs)

    def api_base_url(self):
        return self.base_url

    @classmethod
    def GetDefaultConfig(cls):
        config = Config(Config.hostname, Config.access_key, Config.secret_key)
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
