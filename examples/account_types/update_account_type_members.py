import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

# The account to change membership
account_id = <Account Id>

# The account type that will become the new owner
account_type_id = <Account Type Id>

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

accounts = StaxClient('accounts')

account_type_mappings = [{}]
account_type_mappings[0]["AccountId"] = account_id
account_type_mappings[0]["AccountTypeId"] = account_type_id

response = accounts.UpdateAccountTypeMembers(
	Members=account_type_mappings
)
print(json.dumps(response, indent=4, sort_keys=True))
