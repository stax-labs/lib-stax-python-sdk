"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import datetime
import unittest
import jwt
import botocore

from botocore import UNSIGNED
from botocore.client import Config as BotoConfig
from botocore.stub import Stubber

from staxapp.auth import StaxAuth


class StaxAuthTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.cognito_client = botocore.session.get_session().create_client(
            "cognito-identity",
            region_name="ap-southeast-2",
            config=BotoConfig(signature_version=UNSIGNED),
        )
        self.cognito_stub = Stubber(self.cognito_client)

    def tearDown(self):
        self.cognito_stub.deactivate()

    def testStaxAuthInit(self):
        """
        Test to initialise StaxAuth
        """
        sa = StaxAuth("ApiAuth")
        self.assertEqual(sa.aws_region, "ap-southeast-2")

    def testToken(self):
        """
        Test valid JWT is returned
        """
        sa = StaxAuth("ApiAuth")
        token = sa.id_token_from_cognito()
        jwt_token = jwt.decode(token, verify=False)
        self.assertIn("sub", jwt_token)

    def testCreds(self):
        """
        Test valid credentials are returned
        """
        sa = StaxAuth("ApiAuth")
        token = sa.id_token_from_cognito()
        jwt_token = jwt.decode(token, verify=False)
        self.stub_cognito_creds(jwt_token.get("sub"))
        creds = sa.sts_from_cognito_identity_pool(
            jwt_token.get("sub"), self.cognito_client
        )
        self.assertIn("Credentials", creds)
        self.assertTrue(creds.get("IdentityId").startswith("ap-southeast-2"))

    def stub_cognito_creds(self, token: str):
        sa = StaxAuth("ApiAuth")

        id_response = {"IdentityId": "ap-southeast-2"}
        id_params = {
            "IdentityPoolId": sa.identity_pool,
            "Logins": {
                f"cognito-idp.{sa.aws_region}.amazonaws.com/{sa.user_pool}": token
            },
        }
        self.cognito_stub.add_response("get_id", id_response, id_params)

        id_creds_response = {
            "IdentityId": id_response["IdentityId"],
            "Credentials": {
                "AccessKeyId": "ASIAX000000000000000",
                "SecretKey": "0000000000000000000000000000000000000000",
                "SessionToken": "a-totally-valid-JWT",
                "Expiration": datetime.datetime(2020, 1, 14, 11, 52, 26),
            },
        }
        id_creds_params = {
            "IdentityId": id_response["IdentityId"],
            "Logins": {
                f"cognito-idp.{sa.aws_region}.amazonaws.com/{sa.user_pool}": token
            },
        }
        self.cognito_stub.add_response(
            "get_credentials_for_identity", id_creds_response, id_creds_params
        )

        self.cognito_stub.activate()


if __name__ == "__main__":
    unittest.main()
