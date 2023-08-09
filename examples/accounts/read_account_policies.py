import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The account to read policies for
account_id = <Account Id>

# Read the account policies
accounts = StaxClient("accounts")
response = accounts.ReadAccountPolicyAttachments(
    account_id=account_id
)
print(json.dumps(response, indent=4, sort_keys=True))
