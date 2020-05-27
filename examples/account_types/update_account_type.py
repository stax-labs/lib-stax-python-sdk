import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

# The account type to update
account_type_id = <Account Type Id>
# The new name for the account type
account_type_name = <Account Type Name>

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

accounts = StaxClient('accounts')

response = accounts.UpdateAccountType(
	account_type_id = account_type_id,
	Name = account_type_name
)
print(response)