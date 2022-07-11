import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")
Config.hostname = "api.core.dev.juma.cloud"

# Criteria pull hostname from ssm
# Have multiple clients with different configs
second_config = Config()
second_config.access_key = "2ba09675-7884-4f30-aa74-060f6294c041"
second_config.secret_key = ""
second_config.hostname = "api.core.test.juma.cloud"
# Read all accounts within your Stax Organisation
accounts = StaxClient("accounts")
# response = accounts.ReadAccounts()
# print(response)
second_accounts = StaxClient("accounts", config=second_config)
# s_response = second_accounts.ReadAccounts()
third_config = Config()
third_config.access_key = "67b20d79-b51d-47ce-a420-52b4b7d580b3"
third_config.secret_key = ""
third_accounts = StaxClient("accounts", config=third_config)
t_response = third_accounts.ReadAccounts()
print(json.dumps(t_response, indent=4, sort_keys=True))
