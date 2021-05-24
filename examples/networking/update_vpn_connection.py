import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# updates the attributes of an ACTIVE Stax VPN Connection by providing the `vpn_connection_id` and body properties

networks = StaxClient("networking")

body = {
    "Name": "vpn-gw-name",
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.UpdateVpnConnection(vpn_connection_id="<vpn_connection_uuid>",**body)

print(json.dumps(response, indent=4, sort_keys=True))
