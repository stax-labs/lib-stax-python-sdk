import os
import json

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

body = {
    "Name": "my-own-range"
}
response = networks.UpdateCidrRange(range_id="<range_uuid>", **body)

print(json.dumps(response))