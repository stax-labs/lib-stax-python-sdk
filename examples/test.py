import os
import sys
import boto3

from staxapp.config import Config
from staxapp.openapi import StaxClient
from staxapp.api import Api
from staxapp.exceptions import ApiException

sts = boto3.client("sts")

security_account = '750975847145'
api_token_name = 'dean-token'

response = sts.assume_role(RoleArn=f"arn:aws:iam::{security_account}:role/{api_token_name}-access-role", RoleSessionName=f"{api_token_name}-ssm-role")
assumed_ssm = boto3.client("ssm",
aws_access_key_id=response["Credentials"]["AccessKeyId"],
aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
aws_session_token=response["Credentials"]["SessionToken"]
)
api_token_access_key = assumed_ssm.get_parameter(Name=f"/stax/api-tokens/{api_token_name}/AccessKey", WithDecryption=True)
api_token_secret_key = assumed_ssm.get_parameter(Name=f"/stax/api-tokens/{api_token_name}/SecretKey", WithDecryption=True)

Config.access_key = api_token_access_key['Parameter']['Value']
Config.secret_key = api_token_secret_key['Parameter']['Value']

Config.access_key = 'fake'
Config.secret_key = 'fake'


# fake_client = StaxClient("fake")
client = StaxClient("accounts")

allAccounts = client.ReadAccounts()
print(f'{len(allAccounts["Accounts"])}')
print(client.ReadAccounts(limit=1, offset=0))
print(client.ReadAccounts(account_id="9fc4fd2e-1b4a-49b9-a341-d7ee77ea132d"))
print(client.ReadAccounts(filter="ERROR", account_id="9fc4fd2e-1b4a-49b9-a341-d7ee77ea132d"))


client = StaxClient("workloads")
# client.FakeMethod()
# print(client.ReadCatalogueItems())
response = client.ReadCatalogueItems(catalogue_id='9c4fc016-5221-460d-8bf8-4104178e9e10')
print(client.ReadCatalogueVersion(version_id='545489ae-c090-45cd-9322-42f9b2ed7b6a', catalogue_id='9c4fc016-5221-460d-8bf8-4104178e9e10'))
print(client.ReadCatalogueVersion(version_id='d58ad318-fa36-4310-9766-e7f5e4a34f8d', include_parameters=False, catalogue_id='f13dd683-4aa6-4b88-abc8-ad58a7ee04f9'))

# print(client.DeleteCatalogueVersion(catalogue_id='fake'))
print(client.ReadCatalogueVersion(version_id='d58ad318-fa36-4310-9766-e7f5e4a34f8d', include_parameters=False))

# print(fake_client.ReadAccounts(limit=1, offset=0))
