import os
import json

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

body = {
    "Name": "my-updated-hub-2",
    "Tags": {
        "testing": "yes"
    }
}
response = networks.UpdateHub(hub_id="<hub_uuid>", **body)

print(json.dumps(response))