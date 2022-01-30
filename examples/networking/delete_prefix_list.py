import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# only Stax Direct Connect (DX) Associations with a status of ACTIVE, CREATE_FAILED and DELETE_FAILED can be deleted

networks = StaxClient("networking")

# delete a Stax Prefix List by providing the `prefix_list_uuid`
response = networks.DeletePrefixList(prefix_list_id="<prefix_list_uuid>")

print(json.dumps(response, indent=4, sort_keys=True))
