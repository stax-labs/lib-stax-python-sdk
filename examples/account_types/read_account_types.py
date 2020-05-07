import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all account types within your Stax Organisation
accounts = StaxClient("accounts")
response = accounts.ReadAccountTypes()
print(response)
