import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all users within your Stax Organisation
teams = StaxClient("teams")
response = teams.ReadUsers()
print(response.json())
