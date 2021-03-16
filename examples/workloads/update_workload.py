import json

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = <Access Key>
Config.secret_key = <Secret Key>

# The workload to update
workload_id = <Workload Id>
# The catalogue version id to update the worklaod too
catalogue_version_id = <Catalogue Version Id>

workload_client = StaxClient('workloads')

response = workload_client.UpdateWorkload(workload_id=workload_id, catalogue_version_id=catalogue_version_id)
print(json.dumps(response, indent=4, sort_keys=True))
