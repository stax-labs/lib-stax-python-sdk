import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# if `status` filter is not provided, only resources with the following statuses will be returned by default: ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,UPDATE_IN_PROGRESS

networks = StaxClient("networking")

# read all Stax VPN Customer Gateways in the Organization
response = networks.ReadVpnCustomerGateways()

# read all Stax VPN Customer Gateways in the Organization, filtered by status
response = networks.ReadVpnCustomerGateways(status="ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,DELETE_IN_PROGRESS,DELETED,DELETE_FAILED,UPDATE_IN_PROGRESS")

# read the details of a single Stax VPN Customer Gateway by providing the `vpn_customer_gateway_id`
response = networks.ReadVpnCustomerGateways(vpn_customer_gateway_id="<vpn_customer_gateway_uuid>")

# read all Stax VPN Customer Gateways associated with a Networking Hub by providing the `hub_id`
response = networks.ReadVpnCustomerGateways(hub_id="<hub_uuid>")

print(json.dumps(response, indent=4, sort_keys=True))
