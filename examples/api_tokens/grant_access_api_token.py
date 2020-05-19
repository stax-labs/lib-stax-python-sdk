import sys
import os
import time

from staxapp.config import Config
from staxapp.openapi import StaxClient
from staxapp.exceptions import ApiException

# You can reuse this script whenever you wish to grant an account access to an api token

# Api Token Name
api_token_name = sys.argv[1]

# Account id or name of the account to access the tokens
access_account_id = sys.argv[2]

# Catalogue Name
catalogue_name = 'api-token-access'

workload_client = StaxClient("workloads")
account_client = StaxClient("accounts")


Config.access_key = os.getenv('STAX_ACCESS_KEY')
Config.secret_key = os.getenv('STAX_SECRET_KEY')

try:
				# Ensure that the catalogue exists
				catalogue = workload_client.ReadCatalogueItems(name=catalogue_name, include_parameters="true")['WorkloadCatalogues'][0]['WorkloadCatalogueItems'][0]
except ApiException as e:
				if e.status_code == 404:
						print("You must run create_api_token_catalogue.py before you can run this script")
				else:
						raise e

# Get the security account
accounts = account_client.ReadAccounts()["Accounts"]
for account in accounts:
				if account["Name"] == "security" :
								security_account = account 
				elif account["Id"] == access_account_id or account["Name"] == access_account_id:
								access_account = account["AwsAccountId"]

version = [version for version in catalogue["Versions"] if version["Id"] == catalogue["CatalogueVersionId"]][0]

parameters = []
parameters.append({'Key': "ApiTokenName", 'Value':  api_token_name })
parameters.append({'Key': "AccessAccountId",'Value': access_account })

workload_response = workload_client.CreateWorkload(Name=f"{api_token_name}-access-sdk", 
		CatalogueId=catalogue["Id"],
		AccountId=security_account["Id"],
		Region="ap-southeast-2",
		Parameters=parameters)

# Create a client for tasks
task_client = StaxClient("tasks")

# Wait until status has finished runnig
task={'Status':'RUNNING'}
while task.get('Status') == 'RUNNING':
		time.sleep(2)
		task = task_client.ReadTask(task_id=workload_response["Detail"]["Workload"]['TaskId'])

# If the catalogue version succeeded
if task.get('Status') == 'SUCCEEDED':
			print("Api token access cataologue item successffully created")
else:
			print(f"Api creation wasn't successful. {task}")