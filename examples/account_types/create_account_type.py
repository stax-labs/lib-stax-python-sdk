import os

from staxapp.config import Config
from staxapp.openapi import StaxClient
     
account_type_name = "sdk-2" #<Account Type Name>

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

accounts = StaxClient('accounts')

response = accounts.CreateAccountType(
	Name=account_type_name
)
print(response)