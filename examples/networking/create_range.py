import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API Schema for valid body properties
# creates a CIDR Range within a Stax Networking Hub by providing a `hub_id`

networks = StaxClient("networking")

body = {
    "Cidr": "10.128.0.0/23",
    "Description": "CIDR Range used for team ABCD application 1234",
    "Name": "prod",
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.CreateCidrRange(hub_id="<hub_uuid>", **body)

print(json.dumps(response, indent=4, sort_keys=True))
