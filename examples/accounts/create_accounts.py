import os

from staxapp.config import Config
from staxapp.openapi import StaxClient
     
account_name = <Account Name>
account_type = <Account Type Id>

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

accounts = StaxClient('accounts')

response = accounts.CreateAccount(
		Name=account_name,
		AccountType=account_type,
)
print(response)
