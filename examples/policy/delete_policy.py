import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

policy_id = <Policy Id>

# Delete a policy
organisations = StaxClient("organisations")
response = organisations.DeletePolicy(
	policy_id = policy_id,
)
print(response)
