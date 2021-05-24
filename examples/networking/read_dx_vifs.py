import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# if `status` filter is not provided, only resources with the following statuses will be returned by default: ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,UPDATE_IN_PROGRESS

networks = StaxClient("networking")

# read all Stax Direct Connect (DX) Vifs in the Organization
response = networks.ReadDxVifs()

# read all Stax DX Vifs in the Organization, filtered by status
response = networks.ReadDxVifs(status="ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,DELETE_IN_PROGRESS,DELETED,DELETE_FAILED,UPDATE_IN_PROGRESS")

# read all Stax DX Vifs in a Stax Networking Hub by providing the `hub_id`
response = networks.ReadDxVifs(hub_id="<hub_uuid>")

# read the Stax DX Vifs in a Stax Networking Hub by providing the `hub_id`, filtered by status
response = networks.ReadDxVifs(hub_id="<hub_uuid>",status="DELETED")

# read the details of a single Stax DX Vif by providing the `dx_vif_id`
response = networks.ReadDxVifs(dx_vif_id="<dx_vif_uuid>")

# read the details of a Stax DX Vif by providing the `dx_vif_id`, filtered by status
response = networks.ReadDxVifs(dx_vif_id="<dx_vif_uuid>",status="DELETED")

print(json.dumps(response, indent=4, sort_keys=True))
