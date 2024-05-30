import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

account_name = <Account Name>
account_type = <Account Type Id>
organisational_unit_id = <Organisational Unit Id>

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

accounts = StaxClient('accounts')

response = accounts.CreateAccount(
        Name=account_name,
        AccountType=account_type,
        OrganisationalUnitId=organisational_unit_id,
)
print(json.dumps(response, indent=4, sort_keys=True))
