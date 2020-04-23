import boto3
import sys
import os

if sys.argv.__len__() != 2:
    print("""This script takes 1 positional arguments. 
              To use; in order copy and paste the following in order;
              Deployment Bucket Name
              It will then print out the bucket it was uploaded to""")
# Deployment bucket name
stax_workload_name = sys.argv[1]
# Cloudformation to deploy as a workload
cloudformation_manifest_file = f"./{os.path.dirname(__file__)}/api_token_cfn.yaml"
ssm = boto3.client("ssm")
bucket_name = ssm.get_parameter(Name=f"/workloads/{stax_workload_name}/BucketName", WithDecryption=True)
print(bucket_name["Parameter"]["Value"])
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name["Parameter"]["Value"]).upload_file(cloudformation_manifest_file, 'api_token_cfn.yaml')
