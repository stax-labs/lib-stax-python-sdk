import sys
import boto3
import os
import time

from staxapp.config import Config
from staxapp.openapi import StaxClient
from staxapp.exceptions import ApiException

# Requirements
# - Logged into the deployment bucket account
#	- Logged into the SDK

# This is a one time step to setup the catalogue required

# Deployment bucket name
deployment_bucket_name = <Deployment Bucket Name>

# Path to Cloudformation file to create a catalogue of
# You can download this file from 
cloudformation_manifest_path = <Path to api_token_cfn.yaml>

# Catalogue Name
catalogue_name = 'api-token-access'
# Catalogue version
catalogue_version = '1.0.0'


cfn_name = f'{catalogue_version}-{catalogue_name}.yaml'

Config.access_key = os.getenv('STAX_ACCESS_KEY')
Config.secret_key = os.getenv('STAX_SECRET_KEY')

workload_client = StaxClient("workloads")

try:
				# Check if the workload already exists
				catalogue = workload_client.ReadCatalogueItems(name=catalogue_name)
				print(f"{catalogue['WorkloadCatalogues'][0]['WorkloadCatalogueItems'][0]['Name']} already exists ")
except ApiException as e:
				if e.status_code == 404:
							# Get the AWS name of the deployment bucket
							sts = boto3.client("sts")

							ssm = boto3.client("ssm")
							bucket_name = ssm.get_parameter(Name=f"/workloads/{deployment_bucket_name}/BucketName", WithDecryption=True)

							#Upload the cfn to the deployment bucket
							s3 = boto3.resource('s3')
							s3.Bucket(bucket_name["Parameter"]["Value"]).upload_file(cloudformation_manifest_path, cfn_name)

							# Make the cfn into a workload catalogue item
							manifest_body = f"""Resources:
  - WorkloadSSM:
      Type: AWS::Cloudformation
      TemplateURL: s3://{bucket_name["Parameter"]["Value"]}/{cfn_name}
"""

							catalogue_response = workload_client.CreateCatalogueItem(
								Name=catalogue_name,
								ManifestBody=manifest_body,
								Version=catalogue_version,
								Description='Allows accounts to access specific api-tokens',
								Tags={"Test": "creation"}
							)

							# Create a client for tasks
							task_client = StaxClient("tasks")

							# Wait until status has finished runnig
							task={'Status':'RUNNING'}
							while task.get('Status') == 'RUNNING':
									time.sleep(2)
									task = task_client.ReadTask(task_id=catalogue_response['TaskId'])

							# If the catalogue version succeeded
							if task.get('Status') == 'SUCCEEDED':
										print("Api token access cataologue item successffully created")
							else:
										print(f"Api creation wasn't successful. {task}")
										
				# Handle unknown catalogue error
				else:
							raise e
