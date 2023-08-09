import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The policy to list attachments for
policy_id = <Policy Id>

# Read the policy attachments for the policy
policies = StaxClient("policies")
response = policies.ReadPolicyAttachments(
    policy_id=policy_id,
)
print(json.dumps(response, indent=4, sort_keys=True))
