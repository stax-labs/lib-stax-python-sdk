import os

from stax.config import Config
from stax.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all API tokens within your Stax Organisation
teams = StaxClient("teams")
response = teams.ReadApiTokens()
print(response)
