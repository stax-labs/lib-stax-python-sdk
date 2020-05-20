import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

accounts = StaxClient('accounts')

# An array of Account Type-Policy dicts to enable or an empty array
# 	Properties: AccountTypeId, PolicyId
policies_to_add = <An array of Account type-Policies?>

# An array of Account Type-Policy dicts to disable or an empty arry
policies_to_remove = <An array of Account type-Policies?>

response = accounts.UpdatePolicies(
	AddPolicies= policies_to_add,
	RemovePolicies= policies_to_remove
)
print(response)