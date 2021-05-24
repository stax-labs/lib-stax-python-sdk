import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# only Stax VPN Customer Gateways with a status of ACTIVE, CREATE_FAILED and DELETE_FAILED can be deleted
# Stax VPN Customer Gateways with an active VPN Connection cannot be deleted

networks = StaxClient("networking")

# delete a Stax VPN Customer Gateway by providing the `vpn_customer_gateway_id`
response = networks.DeleteVpnCustomerGateway(vpn_customer_gateway_id="<vpn_customer_gateway_uuid>")

print(json.dumps(response, indent=4, sort_keys=True))
