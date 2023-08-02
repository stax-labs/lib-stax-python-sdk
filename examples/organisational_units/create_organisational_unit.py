import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

organisational_unit_name = <Organisational Unit Name>
parent_organisational_unit_id = <Parent Organisational Unit Id>
tags = {
    "CostCode": "12345"
}

# Create the organisational unit
organisations = StaxClient("organisations")
response = organisations.CreateOrganisationalUnit(
    Name=organisational_unit_name,
    ParentOrganisationalUnitId=parent_organisational_unit_id,
    Tags=tags,
)
print(json.dumps(response, indent=4, sort_keys=True))
