import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The policy to be read
policy_id = <Policy Id>

# Read the Policy
organisations = StaxClient("organisations")
response = organisations.ReadPolicies(policy_id=policy_id)
print(json.dumps(response, indent=4, sort_keys=True))
