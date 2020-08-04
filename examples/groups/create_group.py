import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The name of the group you're creating
group_name = <Group Name>

# Create a Stax groups
teams = StaxClient("teams")
response = teams.CreateGroup(
	Name=group_name
)
print(response.json())
