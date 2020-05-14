import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The name of the token
token_name = <Api Token Name>
# What access the token will have to the api
token_role = <Api Token Role>
# Whether the secret to store the token in ssm params
# Otherwise it will be returned in the response
store_token = <Store Token?>

# Create an Api token with access to your Stax Organisation
teams = StaxClient("teams")
response = teams.CreateApiToken(Name=token_name, Role=token_role, StoreToken=store_token)
print(response)