import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The organisational unit to be read
organisational_unit_id = <Organisational Unit Id>

# Read the organisational unit
organisations = StaxClient("organisations")
response = organisations.ReadOrganisationalUnit(
    organisational_unit_id=organisational_unit_id
)
print(json.dumps(response, indent=4, sort_keys=True))
