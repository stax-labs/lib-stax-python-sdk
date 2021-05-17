import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties

networks = StaxClient("networking")

# create a DNS Resolver within a Stax Networking Hub by providing the `hub_id` and body properties

body = {
    "Name": "dns resolver",
    "NumberOfInterfaces": 2,
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.CreateDnsResolver(hub_id="<hub_uuid>",**body)

print(json.dumps(response, indent=4, sort_keys=True))
