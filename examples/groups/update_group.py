import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# Id of the group to update
group_id = <Group Id>

# Name to rename the group
group_name = <Group Name>

# Create a Stax groups
teams = StaxClient("teams")
response = teams.UpdateGroup(
	group_id=group_id,
	Name=group_name
)
print(response.json())
