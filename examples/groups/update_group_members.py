import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# An array of user memberships dicts to enableor an empty array
# Properties: GroupId(string), UserId(string)
user_membership_to_add = <An array of User Membership?>

# An array of user memberships dicts to disable or an empty arry
user_membership_to_remove = <An array of User Membership?>

# Create a Stax groups
teams = StaxClient("teams")
response = teams.UpdateGroupMembers(
    AddMembers = user_membership_to_add,
    RemoveMembers = user_membership_to_remove
)
print(json.dumps(response, indent=4, sort_keys=True))
