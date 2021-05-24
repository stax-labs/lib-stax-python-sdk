import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties

networks = StaxClient("networking")

# example 1: create a Stax VPN Connection between an existing Stax Networking Hub and a Stax VPN Customer Gateway
# providing a Networking Hub Id will attempt to create a VPN Connection for the VPN Customer Gateway and a Transit Gateway

body = {
    "ImprovedAcceleration": false,
    "Name": "vpn-transit-connection",
    "NetworkingHubId": "<hub_uuid>",
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.CreateVpnConnection(vpn_customer_gateway_id="<vpn_customer_gateway_uuid>",**body)

print(json.dumps(response, indent=4, sort_keys=True))


# example 2: create a Stax VPN Connection between an existing Stax VPC and a Stax VPN Customer Gateway
# providing a VPC Id will attempt to create a VPN Connection for the VPN Customer Gateway and a VPC's Virtual Private Gateway

body = {
    "ImprovedAcceleration": false,
    "Name": "vpn-transit-connection",
    "VpcId": "<vpc_uuid>",
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.CreateVpnConnection(vpn_customer_gateway_id="<vpn_customer_gateway_uuid>",**body)

print(json.dumps(response, indent=4, sort_keys=True))
