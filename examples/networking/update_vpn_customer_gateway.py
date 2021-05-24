import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# update an ACTIVE Stax VPN Customer Gateway by providing the `vpn_customer_gateway_id` and body parameter

networks = StaxClient("networking")

body = {
    "Name": "vpn-gw123",
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.UpdateVpnCustomerGateway(vpn_customer_gateway_id="<<vpn_customer_gateway_uuid>>",**body)

print(json.dumps(response, indent=4, sort_keys=True))
