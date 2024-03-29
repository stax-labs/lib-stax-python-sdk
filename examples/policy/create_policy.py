import json
import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

policy_name = <Policy Name>
policy_description = <Policy Description>
policy = <Policy Json String>
tags = {
    "CostCode": "12345"
}

# Create a policy
organisations = StaxClient("organisations")
response = organisations.CreatePolicy(
    Name=policy_name,
    Description=policy_description,
    Policy=policy,
    Tags=tags,
)
print(json.dumps(response, indent=4, sort_keys=True))
