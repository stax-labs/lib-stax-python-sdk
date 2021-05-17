import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# only Stax Direct Connect (DX) Gateway with a status of ACTIVE, CREATE_FAILED and DELETE_FAILED can be deleted
# Stax DX Gateways with an active DX Connection cannot be deleted

networks = StaxClient("networking")

# delete a Stax DX Gateway by providing the `dx_gateway_id`
response = networks.DeleteDxGateway(dx_gateway_id="<dx_gateway_uuid>")

print(json.dumps(response, indent=4, sort_keys=True))
