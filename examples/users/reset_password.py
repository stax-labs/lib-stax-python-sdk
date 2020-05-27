import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The user id that needs a reset
user_id = <User Id>

teams = StaxClient("teams")
response = teams.UpdateUserPassword(
	user_id=user_id
)
print(response)