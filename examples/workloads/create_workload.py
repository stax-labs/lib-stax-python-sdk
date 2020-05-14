from staxapp.config import Config
from staxapp.openapi import StaxClient

# Requirements
#	- Logged into the SDK

Config.access_key = <Access Key>
Config.secret_key = <Secret Key>


catalogue_id = <Catalogue Id>
workload_name = <Workload Name> 
account_id = <Account Id>
parameter_dict = <Dictionary of Parameters>
tags_dict = <Dictionary of Tags>

workload_client = StaxClient('workloads')

parameters = []
for key, value in parameter_dict.items():
  parameters.append({'Key': key, 'Value': value})

response = workload_client.CreateWorkload(
    Name=workload_name, CatalogueId=catalogue_id, 
    AccountId=account_id, Region='ap-southeast-2',
    Parameters=parameters, Tags=tags_dict
)
print(response)

 