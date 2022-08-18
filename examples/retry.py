import json
import os

from staxapp.config import Config, StaxAPIRetryConfig, StaxAuthRetryConfig
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Retry Config for Stax API calls
retry_config = StaxAPIRetryConfig
retry_config.retry_methods = ('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS')
retry_config.status_codes = (429, 500)

Config.api_retry_config = retry_config

# Retry config for Stax Authentication calls
auth_retry_config = StaxAuthRetryConfig
auth_retry_config.max_attempts = 3

Config.api_auth_retry_config = auth_retry_config

# Read all accounts within your Stax Organisation
accounts = StaxClient("accounts")
response = accounts.ReadAccounts()
print(json.dumps(response, indent=4, sort_keys=True))

