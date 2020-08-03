import os
import json

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

body = {
    "Name": "boston-fern"
}
response = networks.UpdateCidrExclusion(exclusion_id="<exclusion_uuid>", **body)

print(response.json())