import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The policy to be attached
policy_id = <Policy Id>

# Attach a policy to the organisation
organisations = StaxClient("organisations")
response = organisations.AttachPolicy(
    policy_id=policy_id,
)
print(json.dumps(response, indent=4, sort_keys=True))
