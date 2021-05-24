import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# refer to the Stax API schema for valid body properties
# update an ACTIVE Stax Direct Connect (DX) Vif by providing the `dx_vif_id` and body parameter

networks = StaxClient("networking")

body = {
    "JumboMtu": False,
    "Tags": {
        "CostCode": "12345"
    }
}

response = networks.UpdateDxVif(dx_vif_id="<dx_vif_uuid>", **body)

print(json.dumps(response, indent=4, sort_keys=True))
