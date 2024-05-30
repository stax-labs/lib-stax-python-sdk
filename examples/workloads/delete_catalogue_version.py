import json

from staxapp.config import Config
from staxapp.openapi import StaxClient

# Requirements
# - Logged into the SDK

Config.access_key = <Access Key>
Config.secret_key = <Secret Key>

workload_client = StaxClient('workloads')

# Catalogue Name
catalogue_id = <Catalogue Id>
#The Catalogue version to delete
catalogue_version_id = <Catalogue Version>

response = workload_client.DeleteCatalogueVersion(
    catalogue_id=catalogue_id,
    version_id=catalogue_version_id
)
print(json.dumps(response, indent=4, sort_keys=True))
