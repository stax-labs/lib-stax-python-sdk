import os

from staxapp.config import Config
from staxapp.openapi import StaxClient
     
account_type_id = <Account Type Id>

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

accounts = StaxClient('accounts')

response = accounts.DeleteAccountType(
	account_type_id=account_type_id
)
print(response.json())