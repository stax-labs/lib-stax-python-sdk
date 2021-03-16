import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The policy to be updated
policy_id = <Policy Id>

policy_description = <Policy Description>

policy = <Policy Json>

# Update a policy
organisations = StaxClient("organisations")
response = organisations.UpdatePolicy(
	policy_id = policy_id,
	Description=policy_description,
	Policy=policy,
)
print(json.dumps(response, indent=4, sort_keys=True))
