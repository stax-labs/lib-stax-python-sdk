import os
import json

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

# read all exclusions in the organisation, optionally filtered by statuses
response = networks.ReadCidrExclusions(status="ACTIVE")

print(json.dumps(response, indent=4, sort_keys=True))