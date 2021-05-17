import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API Schema for valid body properties

networks = StaxClient("networking")

# example 1: create a Stax Direct Connect (DX) Gateway

body = {
    "Gateway": {
        "AccountId": "<stax_account_uuid>",
        "Asn": 64512,
        "GatewayType": "TRANSIT",
        "Name": "Prod Gateway",
    }
}

response = networks.CreateDxResource(**body)

print(json.dumps(response, indent=4, sort_keys=True))

# example 2: create a Stax DX Gateway and associated DX Vif

body = {
    "Gateway": {
        "AccountId": "<stax_account_uuid>",
        "Asn": 64512,
        "GatewayType": "TRANSIT",
        "Name": "Prod Gateway",
    },
    "Vif": {
        "Asn": 64513,
        "AwsConnectionId": "dx-con-xxxxxx",
        "AwsRouterIp": "192.168.0.2/30",
        "BgpAuthKey": "secret",
        "JumboMtu": True,
        "Name": "Prod VIF",
        "RouterIp": "192.168.0.1/30",
        "Tags": {
            "CostCode": "12345"
        },
        "Vlan": 4000,
    },
}

response = networks.CreateDxResource(**body)

print(json.dumps(response, indent=4, sort_keys=True))


# example 3: create a Stax DX Vif and attach to an existing DX Gateway by provided the Dx Gateway Id

body = {
    "Vif": {
        "Asn": 64513,
        "AwsConnectionId": "dx-con-xxxxxx",
        "AwsRouterIp": "192.168.0.2/30",
        "DxGatewayId": "<dx_gateway_uuid>",
        "BgpAuthKey": "secret",
        "JumboMtu": True,
        "Name": "Prod VIF",
        "RouterIp": "192.168.0.1/30",
        "Tags": {
            "CostCode": "12345"
        },
        "Vlan": 4000,
    }
}

response = networks.CreateDxResource(**body)

print(json.dumps(response, indent=4, sort_keys=True))
