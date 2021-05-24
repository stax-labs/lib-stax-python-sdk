import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# if `status` filter is not provided, only resources with the following statuses will be returned by default: ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,UPDATE_IN_PROGRESS

networks = StaxClient("networking")

# read all Stax Direct Connect (DX) Gateways in the Organization
response = networks.ReadDxGateways()

# read all Stax DX Gateways in the Organization, filtered by statuses
response = networks.ReadDxGateways(status="ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,DELETE_IN_PROGRESS,DELETED,DELETE_FAILED,UPDATE_IN_PROGRESS")

# read all Stax DX Gateways within a Stax Networking Hub by providing the `hub_id`
response = networks.ReadDxGateways(hub_id="<hub_uuid>")

# read all Stax DX Gateways within a Stax Networking Hub by providing the `hub_id`, filtered by status
response = networks.ReadDxGateways(hub_id="<hub_uuid>",status="DELETED")

# read the details of a single Stax DX Gateway by providing the `dx_gateway_id`
response = networks.ReadDxGateways(dx_gateway_id="<dx_gateway_uuid>")

# read the details of a single Stax DX Gateway by providing the `dx_gateway_id`, filtered by statuses
response = networks.ReadDxGateways(dx_gateway_id="<dx_gateway_uuid>",status="DELETED")

print(json.dumps(response, indent=4, sort_keys=True))
