import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties

networks = StaxClient("networking")

# example 1: create a Stax Hub Prefix List

body = {
    "Entries": [
        "192.168.0.1/32",
        "192.168.0.2/32"
    ],
    "MaxEntries": 3,
    "Name": "example",
    "RouteTableTypes": [
        "INFRASTRUCTURE",
        "ISOLATED"
    ],
    "Tags": {
        "CostCode": "12345"
    },
    "TargetId": "ec5eaa8f-da06-4935-b5ce-05bd957c8bdc",
    "TargetType": "VPC",
    "Zones": [
        "ZONE1",
        "ZONE2"
    ]
}

response = networks.CreateHubPrefixList(hub_id="<hub_uuid>",**body)

print(json.dumps(response, indent=4, sort_keys=True))

# example 2: create a Stax VPC Prefix List

body = {
    "Entries": [
        "192.168.0.1/32",
        "192.168.0.2/32"
    ],
    "MaxEntries": 3,
    "Name": "example",
    "SubnetTypes": [
        "PRIVATE",
        "RESTRICTED"
    ],
    "Tags": {
        "CostCode": "12345"
    },
    "VpcIds": [
        "a7220870-40fe-4235-abb3-4d42af0336c2",
        "7e542285-8b90-4b57-81e1-96e87e5ee443"
    ],
    "VpcTypes": [
        "TRANSIT",
        "ISOLATED"
    ],
    "Zones": [
        "ZONE1",
        "ZONE2"
    ]
}

response = networks.CreateVpcPrefixList(hub_id="<hub_uuid>",**body)

print(json.dumps(response, indent=4, sort_keys=True))