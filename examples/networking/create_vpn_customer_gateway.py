import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# create a Stax VPN Customer Gateway by providing the body parameter

networks = StaxClient("networking")

body = {
    "AccountId": "<stax_account_uuid>",
    "Asn": 64513,
    "IpAddress": "1.1.1.1",
    "Name": "vpn-gw",
    "Region": "ap-northeast-1",
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.CreateVpnCustomerGateway(**body)

print(json.dumps(response, indent=4, sort_keys=True))
