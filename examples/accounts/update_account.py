import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

# The account you want to update
account_id = <Account Id>

#To change account types include an account type id
account_type_id = <Account Type Id?>

# To change the tags include a dictionary of tags
tags_dict = <A dictionary of tags?>

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

accounts = StaxClient('accounts')

update_properties = {}
if tags_dict:
    update_properties.update(tags)
if account_type_id:
    update_properties["AccountType"] = account_type_id

response = accounts.UpdateAccount(
        account_id=account_id,
        **update_properties
)
print(json.dumps(response, indent=4, sort_keys=True))
