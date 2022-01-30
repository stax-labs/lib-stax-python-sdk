import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

# read all Stax Prefix Lists in the Organization
response = networks.ReadPrefixLists()

# read all Stax Prefix Lists in the Organization, filtered by statuses
response = networks.ReadPrefixLists(status="ACTIVE,CREATE_IN_PROGRESS,CREATE_FAILED,DELETE_IN_PROGRESS,DELETED,DELETE_FAILED,UPDATE_IN_PROGRESS")

# read all Stax Prefix Lists in a Stax Networking Hub by providing the `hub_id`
response = networks.ReadHubPrefixLists(hub_id="<hub_uuid>")

# read the Stax Prefix Lists in a Stax Networking Hub by providing the `hub_id`, filtered by status
response = networks.ReadHubPrefixLists(hub_id="<hub_uuid>",status="DELETED")

# read the details of a single Stax Prefix List by providing the `prefix_list_uuid`
response = networks.ReadPrefixList(prefix_list_id="<prefix_list_uuid>")

print(json.dumps(response, indent=4, sort_keys=True))
