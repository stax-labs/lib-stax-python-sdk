import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

# read all hubs, or optionally provide a `hub_id` as an argument
response = networks.ReadHubs()
print(json.dumps(response, indent=4, sort_keys=True))

# read hubs by statuses
response = networks.ReadHubs(status="DELETED,ACTIVE")
print(response.json()))