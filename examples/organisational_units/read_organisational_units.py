import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Read all organisational units within your Stax Organisation
organisations = StaxClient("organisations")
response = organisations.ReadOrganisationalUnits()
print(json.dumps(response, indent=4, sort_keys=True))
