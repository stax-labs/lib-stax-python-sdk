import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# if `status` filter is not provided, only resources with the following statuses will be returned by default: ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,UPDATE_IN_PROGRESS

networks = StaxClient("networking")

# read all Stax Direct Connect (DX) Associations in the Organization
response = networks.ReadDxAssociations()

# read all Stax DX Associations in the Organization, filtered by statuses
response = networks.ReadDxAssociations(status="ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,DELETE_IN_PROGRESS,DELETED,DELETE_FAILED,UPDATE_IN_PROGRESS")

# read the Stax DX Associations in a Stax Networking Hub by providing the `hub_id`
response = networks.ReadDxAssociations(hub_id="<hub_uuid>")

# read the Stax DX Associations in a Stax Networking Hub by providing the `hub_id`, filtered by status
response = networks.ReadDxAssociations(hub_id="<hub_uuid>",status="DELETED")

# read the details of a single Stax DX Association by providing the `dx_association_uuid`
response = networks.ReadDxAssociations(dx_association_id="<dx_association_uuid>")

# read the details of a single Stax DX Association by providing the `dx_association_uuid`, filtered by status
response = networks.ReadDxAssociations(dx_association_id="<dx_association_uuid>",status="DELETED")

print(json.dumps(response, indent=4, sort_keys=True))
