import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The user id to resend invite
user_id = <User Id>

# Not required just show how properties are changed
user_role = <New Role>
user_status = <New Status>


# Update a Stax User
teams = StaxClient("teams")
response = teams.UpdateUser(
	user_id = user_id,
	Role = user_role,
	Status = user_status
)
print(response.json())