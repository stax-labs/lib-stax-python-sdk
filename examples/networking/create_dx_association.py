import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties

networks = StaxClient("networking")

# example 1: create a Stax Direct Connect (DX) association between a Networking Hub and a DX Gateway
# providing a Networking Hub Id will attempt to associate the DX Gateway that contains Transit VIFs to the Networking Hub's Transit Gateway

body = {
    "NetworkingHubId": "<hub_uuid>",
    "Prefixes": [
        "192.168.0.0/24",
        "192.168.1.0/24"
    ]
}

response = networks.CreateDxAssociation(dx_gateway_id="<dx_gateway_uuid>",**body)

print(json.dumps(response, indent=4, sort_keys=True))


# example 2: create a Stax DX association between a Stax Networking Hub's VPC and a Stax DX Gateway
# providing a VPC Id will attempt to associate the DX Gateway that contains private VIFs to the VPCs virtual private gateway

body = {
    "VpcId": "<vpc_uuid>",
    "Prefixes": [
        "192.168.0.0/24",
        "192.168.1.0/24"
    ]
}

response = networks.CreateDxAssociation(dx_gateway_id="<dx_gateway_uuid>",**body)

print(json.dumps(response, indent=4, sort_keys=True))
