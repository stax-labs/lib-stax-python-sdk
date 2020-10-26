from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = <Access Key>
Config.secret_key = <Secret Key>

workload_id = <Workload Id> 

workload_client = StaxClient('workloads')

response = workload_client.DeleteWorkload(workload_id=workload_id)
print(response.json())