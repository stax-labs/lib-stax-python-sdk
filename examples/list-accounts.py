import os

from stax.config import Config
from stax.openapi import StaxClient

Config.access_key = os.getenv("TEST_ACCESS_KEY")
Config.secret_key = os.getenv("TEST_SECRET_KEY")

accounts = StaxClient("accounts")
foo = accounts.ReadAccounts(include_tags=True, filter="ACTIVE")
print(f"{foo}")
