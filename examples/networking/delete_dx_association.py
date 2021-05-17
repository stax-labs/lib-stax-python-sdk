import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# only Stax Direct Connect (DX) Associations with a status of ACTIVE, CREATE_FAILED and DELETE_FAILED can be deleted

networks = StaxClient("networking")

# delete a Stax DX Association by providing the `dx_association_uuid`
response = networks.DeleteDxAssociation(dx_association_id="<dx_association_uuid>")

print(json.dumps(response, indent=4, sort_keys=True))
