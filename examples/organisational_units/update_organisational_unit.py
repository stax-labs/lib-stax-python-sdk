import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The organisational unit to be updated
organisational_unit_id = <Organisational Unit Id>

organisational_unit_name = <Organisational Unit Name>
tags = {
    "CostCode": "12345"
}

# Update the organisational unit
organisations = StaxClient("organisations")
response = organisations.UpdateOrganisationalUnit(
    organisational_unit_id=organisational_unit_id,
    Name=organisational_unit_name,
    Tags=tags,
)
print(json.dumps(response, indent=4, sort_keys=True))
