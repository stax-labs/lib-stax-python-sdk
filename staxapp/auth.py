#!/usr/local/bin/python3
from datetime import datetime, timezone

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
from botocore import UNSIGNED
from botocore.client import Config as BotoConfig
from botocore.exceptions import ClientError
from warrant import AWSSRP

from staxapp.config import Config as StaxConfig
from staxapp.exceptions import InvalidCredentialsException


class StaxAuth:
    def __init__(self, config_branch):
        config = StaxConfig.api_config

        self.identity_pool = config.get(config_branch).get("identityPoolId")
        self.user_pool = config.get(config_branch).get("userPoolId")
        self.client_id = config.get(config_branch).get("userPoolWebClientId")
        self.aws_region = config.get(config_branch).get("region")

    def requests_auth(self, username, password, **kwargs):
        if username is None:
            raise InvalidCredentialsException(
                "Please provide an Access Key to your config"
            )
        if password is None:
            raise InvalidCredentialsException(
                "Please provide a Secret Key to your config"
            )

        id_token = self.id_token_from_cognito(username, password, **kwargs)
        id_creds = self.sts_from_cognito_identity_pool(id_token, **kwargs)
        auth = self.sigv4_signed_auth_headers(id_creds)

        StaxConfig.expiration = id_creds.get("Credentials").get("Expiration")
        StaxConfig.auth = auth

        return StaxConfig.auth

    def id_token_from_cognito(
        self, username=None, password=None, srp_client=None, **kwargs
    ):
        token = None
        if not srp_client:
            srp_client = boto3.client(
                "cognito-idp",
                region_name=self.aws_region,
                config=BotoConfig(signature_version=UNSIGNED),
            )
        aws = AWSSRP(
            username=username,
            password=password,
            pool_id=self.user_pool,
            client_id=self.client_id,
            client=srp_client,
        )
        try:
            tokens = aws.authenticate_user()
        except ClientError as e:
            if e.response["Error"]["Code"] == "NotAuthorizedException":
                raise InvalidCredentialsException(
                    message=str(e), detail="Please check your Secret Key is correct"
                )
            elif e.response["Error"]["Code"] == "UserNotFoundException":
                raise InvalidCredentialsException(
                    message=str(e),
                    detail="Please check your Access Key, that you have created your Api Token and that you are using the right STAX REGION",
                )
            else:
                raise InvalidCredentialsException(
                    f"Unexpected Client Error. Error details: {e}"
                )
        token = tokens["AuthenticationResult"]["IdToken"]
        return token

    def sts_from_cognito_identity_pool(self, token, cognito_client=None, **kwargs):
        if not cognito_client:
            cognito_client = boto3.client(
                "cognito-identity",
                region_name=self.aws_region,
                config=BotoConfig(signature_version=UNSIGNED),
            )
        try:
            id = cognito_client.get_id(
                IdentityPoolId=self.identity_pool,
                Logins={
                    f"cognito-idp.{self.aws_region}.amazonaws.com/{self.user_pool}": token
                },
            )
            id_creds = cognito_client.get_credentials_for_identity(
                IdentityId=id["IdentityId"],
                Logins={
                    f"cognito-idp.{self.aws_region}.amazonaws.com/{self.user_pool}": token
                },
            )
        except ClientError as e:
            raise InvalidCredentialsException(
                f"Unexpected Client Error. Error details: {e}"
            )
        return id_creds

    def sigv4_signed_auth_headers(self, id_creds):
        auth = AWSRequestsAuth(
            aws_access_key=id_creds.get("Credentials").get("AccessKeyId"),
            aws_secret_access_key=id_creds.get("Credentials").get("SecretKey"),
            aws_token=id_creds.get("Credentials").get("SessionToken"),
            aws_host=f"{StaxConfig.hostname}",
            aws_region=self.aws_region,
            aws_service="execute-api",
        )
        return auth


class RootAuth:
    @staticmethod
    def requests_auth(username, password, **kwargs):
        if StaxConfig.expiration and StaxConfig.expiration > datetime.now(timezone.utc):
            return StaxConfig.auth

        return StaxAuth("JumaAuth").requests_auth(username, password, **kwargs)


class ApiTokenAuth:
    @staticmethod
    def requests_auth(username, password, **kwargs):
        if StaxConfig.expiration and StaxConfig.expiration > datetime.now(timezone.utc):
            return StaxConfig.auth

        return StaxAuth("ApiAuth").requests_auth(username, password, **kwargs)
