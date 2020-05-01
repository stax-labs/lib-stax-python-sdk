import os
import sys

from stax.config import Config
from stax.openapi import StaxClient


Config.access_key = os.getenv("ACCESS_KEY")
Config.secret_key = os.getenv("SECRET_KEY")

client = StaxClient("accounts")
allAccounts = client.ReadAccounts()
print(f'{len(allAccounts["Accounts"])}')
print(client.ReadAccounts(limit=1, offset=0))
print(client.ReadAccounts(account_id="9fc4fd2e-1b4a-49b9-a341-d7ee77ea132d"))
print(client.ReadAccounts(filter="ERROR", account_id="9fc4fd2e-1b4a-49b9-a341-d7ee77ea132d"))

client = StaxClient("workloads")
print(client.ReadCatalogueVersion(version_id='d58ad318-fa36-4310-9766-e7f5e4a34f8d', catalogue_id='f13dd683-4aa6-4b88-abc8-ad58a7ee04f9'))
print(client.ReadCatalogueVersion(version_id='d58ad318-fa36-4310-9766-e7f5e4a34f8d', include_parameters=False, catalogue_id='f13dd683-4aa6-4b88-abc8-ad58a7ee04f9'))

client = StaxClient('fake')
print(client.ReadCatalogueVersion(version_id='d58ad318-fa36-4310-9766-e7f5e4a34f8d', include_parameters=False))
