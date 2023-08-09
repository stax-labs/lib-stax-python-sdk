import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The policy attachment to be detached
policy_attachment_id = <Policy Attachment Id>

# Detach a policy attachment
policies = StaxClient("policies")
response = policies.DetachPolicy(
    policy_attachment_id=policy_attachment_id,
)
print(json.dumps(response, indent=4, sort_keys=True))
