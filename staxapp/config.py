import logging
import os
import platform as sysinfo
from time import sleep

import requests

import staxapp
from staxapp.exceptions import ApiException

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("nose").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


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
    hostname = f"api.{STAX_REGION}"
    org_id = None
    auth = None
    expiration = None
    load_live_schema = True

    platform = sysinfo.platform()
    python_version = sysinfo.python_version()
    sdk_version = staxapp.__version__

    @classmethod
    def set_config(cls):
        cls.base_url = f"https://{cls.hostname}/{cls.API_VERSION}"
        config_url = f"{cls.api_base_url()}/public/config"
        backoff_rate = float(os.environ.get("CONFIG_BACKOFF_RATE", "2"))
        initial_wait = float(os.environ.get("CONFIG_INITIAL_WAIT", "0.5"))
        retry_limit = int(os.environ.get("CONFIG_RETRY_LIMIT", "4"))
        delay = initial_wait
        config_response = requests.get(config_url)
        while config_response.status_code == 403 and retry_limit != 0:
            retry_limit -= 1
            sleep(delay)
            delay *= backoff_rate
            logging.warning(
                "public config URL is likely affected by WAF protections, retrying"
            )
            logging.warning(f"{retry_limit} attempts left")
            config_response = requests.get(config_url)
        try:
            config_response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"{config_response.status_code}: {config_response.json()}")

            raise ApiException(
                str(e), config_response, detail=" Could not load API config."
            )

        cls.api_config = config_response.json()

    @classmethod
    def init(cls, config=None):
        if cls._initialized:
            return

        if not config:
            cls.set_config()

        cls._initialized = True

    @classmethod
    def api_base_url(cls):
        return cls.base_url

    @classmethod
    def branch(cls):
        return os.getenv("STAX_BRANCH", "master")

    @classmethod
    def schema_url(cls):
        return f"{cls.base_url}/public/api-document"

    @classmethod
    def get_auth_class(cls):
        if cls.auth_class is None:
            from staxapp.auth import ApiTokenAuth

            cls.auth_class = ApiTokenAuth
        return cls.auth_class


Config.init()
