import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Id of the group to delete
group_id = <Group Id>

# Create a Stax groups
teams = StaxClient("teams")
response = teams.DeleteGroup(
	group_id=group_id
)
print(response)
