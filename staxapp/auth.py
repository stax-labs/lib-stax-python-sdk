#!/usr/local/bin/python3
from datetime import datetime, timedelta, timezone

import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
from botocore import UNSIGNED
from botocore.client import Config as BotoConfig
from botocore.exceptions import ClientError

from staxapp.aws_srp import AWSSRP
from staxapp.config import Config as StaxConfig
from staxapp.exceptions import InvalidCredentialsException


class StaxAuth:
    def __init__(self, config_branch: str, config: StaxConfig, max_retries: int = 5):
        self.config = config
        api_config = self.config.api_config
        self.identity_pool = api_config.get(config_branch).get("identityPoolId")
        self.user_pool = api_config.get(config_branch).get("userPoolId")
        self.client_id = api_config.get(config_branch).get("userPoolWebClientId")
        self.aws_region = api_config.get(config_branch).get("region")
        self.max_retries = max_retries

    def requests_auth(self, **kwargs):
        username = self.config.access_key
        password = self.config.secret_key
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

        self.config.expiration = id_creds.get("Credentials").get("Expiration")
        self.config.auth = auth

        return self.config.auth

    def id_token_from_cognito(
        self, username=None, password=None, srp_client=None, **kwargs
    ):
        token = None
        if not srp_client:
            srp_client = boto3.client(
                "cognito-idp",
                region_name=self.aws_region,
                config=BotoConfig(
                    signature_version=UNSIGNED,
                    retries={"max_attempts": self.max_retries, "mode": "standard"},
                ),
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
                    detail=f"Please check your Access Key, that you have created your Api Token and that you are using the right STAX REGION",
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
                config=BotoConfig(
                    signature_version=UNSIGNED,
                    retries={"max_attempts": self.max_retries, "mode": "standard"},
                ),
            )

        for i in range(self.max_retries):
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
                break
            except ClientError as e:
                # AWS eventual consistency, attempt to retry up to n (max_retries) times
                if "Couldn't verify signed token" in str(e):
                    continue
                else:
                    raise InvalidCredentialsException(
                        f"Unexpected Client Error. Error details: {e}"
                    )
        else:
            raise InvalidCredentialsException(
                "Retries Exceeded: Unexpected Client Error"
            )

        return id_creds

    def sigv4_signed_auth_headers(self, id_creds):
        auth = AWSRequestsAuth(
            aws_access_key=id_creds.get("Credentials").get("AccessKeyId"),
            aws_secret_access_key=id_creds.get("Credentials").get("SecretKey"),
            aws_token=id_creds.get("Credentials").get("SessionToken"),
            aws_host=f"{self.config.hostname}",
            aws_region=self.aws_region,
            aws_service="execute-api",
        )
        return auth


class RootAuth:
    @staticmethod
    def requests_auth(username, password, **kwargs):
        if StaxConfig.expiration and StaxConfig.expiration > datetime.now(timezone.utc):
            return StaxConfig.auth
        config = StaxConfig.GetDefaultConfig()
        config.init()
        config.access_key = username
        config.secret_key = password
        return StaxAuth("JumaAuth", config).requests_auth(**kwargs)


class ApiTokenAuth:
    @staticmethod
    def requests_auth(config: StaxConfig, **kwargs):
        # Minimize the potential for token to expire while still being used for auth (say within a lambda function)
        print(config.api_auth_retry_config.token_expiry_threshold)
        if config.expiration and config.expiration - timedelta(
            minutes=config.api_auth_retry_config.token_expiry_threshold
        ) > datetime.now(timezone.utc):
            return config.auth
        return StaxAuth(
            "ApiAuth",
            config,
            max_retries=config.api_auth_retry_config.max_attempts,
        ).requests_auth(**kwargs)
