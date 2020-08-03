import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

accounts = StaxClient('accounts')

# An array of access_role dicts to enable or empty array
# 	Properties: RoleName, AccountTypeId, GroupId
access_roles_to_add = <An array of access_roles?>

# # An array of access_role dicts to disable or empty arry
access_roles_to_remove = <An array of access_roles?>


response = accounts.UpdateAccountTypeAccess(
	AddRoles= access_roles_to_add,
	RemoveRoles=access_roles_to_remove
)
print(response.json())