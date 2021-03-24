import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all accounts within your Stax Organisation
accounts = StaxClient("accounts")
response = accounts.ReadAccounts()
print(json.dumps(response, indent=4, sort_keys=True))

# Read all active accounts within your Stax Organisation and include tags in the response
accounts = StaxClient("accounts")
response = accounts.ReadAccounts(filter="ACTIVE", include_tags=True)
print(json.dumps(response, indent=4, sort_keys=True))
