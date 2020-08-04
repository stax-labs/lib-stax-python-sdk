
from staxapp.config import Config
from staxapp.openapi import StaxClient
from staxapp.api import Api

# Requirements
#	- Logged into the SDK


Config.access_key = <Access Key>
Config.secret_key = <Secret Key>

catalogue_id = <Catalogue Id>

workload_client = StaxClient("workloads")

response = workload_client.DeleteCatalogueItem(catalogue_id=catalogue_id)
print(response.json())