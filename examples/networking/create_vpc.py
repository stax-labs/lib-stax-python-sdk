import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API Schema for valid body properties
# create a VPC within a Stax Networking Hub by providing the `hub_id` and body properties

networks = StaxClient("networking")

body = {
    "AccountId": "<stax_account_uuid>",
    "CidrRangeId": "<range_uuid>",
    "CreateCloudwatchVpcFlowlogs": True,
    "CreateInternetGateway": True,
    "CreateVirtualPrivateGateway": False,
    "Description": "VPC for a non-prod microservice",
    "GatewayEndpoints": [
        "s3"
    ],
    "Name": "dev-ms-customers",
    "PhzPrefix": "dev",
    "Region": "ap-northeast-1",
    "Size": "SMALL",
    "Tags": {
        "CostCode": "12345"
    },
    "Type": "ISOLATED",
    "VirtualPrivateGatewayAsn": 64513,
    "Zone": "my-zone"
}

response = networks.CreateVpc(hub_id="<hub_uuid>", **body)

print(json.dumps(response, indent=4, sort_keys=True))
