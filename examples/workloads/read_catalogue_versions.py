import json

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = <Access key>
Config.secret_key = <Secret key>

# Catalogue Id
catalogue_id = <Catalogue Id>
#Version Id
version_id = <Catalogue Version>

workload_client = StaxClient("workloads")
response = workload_client.ReadCatalogueVersion(catalogue_id=catalogue_id, version_id=version_id)

print(json.dumps(response, indent=4, sort_keys=True))
