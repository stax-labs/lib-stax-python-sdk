import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The token to delete's AccessKey
access_key = <Access Key>

# Delete an Api Token
teams = StaxClient("teams")
response = teams.DeleteApiToken(AccessKey=access_key)

print(json.dumps(response, indent=4, sort_keys=True))
