import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

# The policy to be attached
policy_id = <Policy Id>

# The target to attach the Policy to
account_id = <Account Id>
organisational_unit_id = <Organisational Unit Id>

# Attach a policy to the Account
policies = StaxClient("policies")
response = policies.AttachPolicy(
    policy_id=policy_id,
    AccountId=account_id,
)
print(json.dumps(response, indent=4, sort_keys=True))

# Attach a policy to the Organisational Unit
policies = StaxClient("policies")
response = policies.AttachPolicy(
    policy_id=policy_id,
    OrganisationalUnitId=organisational_unit_id,
)
print(json.dumps(response, indent=4, sort_keys=True))
