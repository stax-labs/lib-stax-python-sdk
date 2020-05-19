import boto3
import sys
import os

# The name of the api token
api_token_name = <API_TOKEN_NAME>
# The security account id
security_account = <SECURITY_ACCOUNT_AWS_ID>
# The account that can access the security tokens that you are logged in as
access_account = <ACCOUNT_AWD_ID>

sts = boto3.client("sts")

response = sts.assume_role(RoleArn=f"arn:aws:iam::{security_account}:role/{api_token_name}-access-role", RoleSessionName=f"{api_token_name}-ssm-role")
assumed_ssm = boto3.client("ssm",
aws_access_key_id=response["Credentials"]["AccessKeyId"],
aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
aws_session_token=response["Credentials"]["SessionToken"]
)
api_token_access_key = assumed_ssm.get_parameter(Name=f"/stax/api-tokens/{api_token_name}/AccessKey", WithDecryption=True)
api_token_secret_key = assumed_ssm.get_parameter(Name=f"/stax/api-tokens/{api_token_name}/SecretKey", WithDecryption=True)
print(f"Access Key: {api_token_access_key['Parameter']['Value']}")
print(f"Secret Key: {api_token_secret_key['Parameter']['Value']}")

