import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The user's first name
first_name = <User's first Name>

# The user's second name
last_name = <User's last Name>

# The email for the user
user_email = <User's Email>

# Create a Stax User
teams = StaxClient("teams")
response = teams.CreateUser(
    FirstName = first_name,
    LastName = last_name,
    Email = user_email
)
print(json.dumps(response, indent=4, sort_keys=True))
