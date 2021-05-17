import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# if `status` filter is not provided, only resources with the following statuses will be returned by default: ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,UPDATE_IN_PROGRESS

networks = StaxClient("networking")

# read all Stax VPCs in the Organization
response = networks.ReadVpcs()

# read all Stax VPCs in the Organization, filtered by status
response = networks.ReadVpcs(status="ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,DELETE_IN_PROGRESS,DELETED,DELETE_FAILED,UPDATE_IN_PROGRESS")

# read all Stax VPCs in the Organization, filtered by type/s
response = networks.ReadVpcs(type="TRANSIT,ISOLATED,SHAREDSERVICES,FLAT")

# read all Stax VPCs, filtered by status and type
response = networks.ReadVpcs(status="ACTIVE",type="TRANSIT")

# read the details of a Stax VPC by providng the `vpc_id`
response = networks.ReadVpcs(vpc_id="<vpc_uuid>")

# read the details of a Stax VPC by providng the `vpc_id`, filtered by status
response = networks.ReadVpcs(vpc_id="<vpc_uuid>",status="CREATE_IN_PROGRESS")

print(json.dumps(response, indent=4, sort_keys=True))
