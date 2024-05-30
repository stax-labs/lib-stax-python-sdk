import boto3
import json

from staxapp.config import Config
from staxapp.openapi import StaxClient

# Requirements
# - Logged into the deployment bucket account
# - Logged into the SDK

Config.access_key = <Access Key>
Config.secret_key = <Secret Key>

# Deployment bucket name
deployment_bucket_name = <Deployment bucket workload name>
# Path to Cloudformation file to deploy as a workload
cloudformation_manifest_path = <Cloudformation File>
# Catalogue Id
catalogue_id = <Catalogue Id>
#The new Catalogue version
catalogue_version = <Catalogue Version>

workload_client = StaxClient('workloads')

# Get the AWS name of the deployment bucket
ssm = boto3.client("ssm")
bucket_name = ssm.get_parameter(Name=f"/workloads/{deployment_bucket_name}/BucketName", WithDecryption=True)

#Upload the cfn to the deployment bucket
s3 = boto3.resource('s3')
cfn_name = f'{catalogue_version}-{catalogue_name}.yaml'
s3.Bucket(bucket_name["Parameter"]["Value"]).upload_file(cloudformation_manifest_path, cfn_name)

# # Invoke the Stax SDK
workload_client = StaxClient("workloads")

# Make the cfn into a workload catalogue item
manifest_body = f"""Resources:
  - WorkloadSSM:
      Type: AWS::Cloudformation
      TemplateURL: s3://{bucket_name["Parameter"]["Value"]}/{cfn_name}
"""

response = workload_client.CreateCatalogueVersion(
    ManifestBody=manifest_body,
    Version=catalogue_version,
    Description='Updating versions via sdk',
    catalogue_id=catalogue_id
)
print(json.dumps(response, indent=4, sort_keys=True))
