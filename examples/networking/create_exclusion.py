import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

# refer to the Stax API Schema for valid body properties
# create a CIDR Exclusion within a Stax Networking Hub by providing the `hub_id` and body properties

body = {
    "Cidr": "10.128.0.0/19",
    "Description": "This Reservation blocks out existing legacy VPCs",
    "Name": "legacy-vpcs",
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.CreateCidrExclusion(hub_id="<hub_uuid>", **body)

print(json.dumps(response, indent=4, sort_keys=True))
