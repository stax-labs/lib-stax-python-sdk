import os

from stax.config import Config
from stax.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all policies within your Stax Organisation
organisations = StaxClient("organisations")
response = organisations.ReadPolicies()
print(response)
