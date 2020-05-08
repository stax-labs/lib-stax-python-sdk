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
from botocore.stub import Stubber, ANY

from staxapp.auth import StaxAuth
from staxapp.exceptions import InvalidCredentialsException


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

        self.aws_srp_client = botocore.session.get_session().create_client(
            "cognito-idp",
            region_name="ap-southeast-2",
            config=BotoConfig(signature_version=UNSIGNED),
        )
        self.aws_srp_stubber = Stubber(self.aws_srp_client)

    def tearDown(self):
        self.cognito_stub.deactivate()
        self.aws_srp_stubber.deactivate()

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
        self.stub_aws_srp(sa, "valid_username")
        token = sa.id_token_from_cognito(
            username="valid_username", password="correct", client=self.aws_srp_client
        )
        self.assertEqual(token, "valid_token")

    def testCredentialErrors(self):
        """
        Test that boto errors are caught and converted to InvalidCredentialExceptions
      """

        sa = StaxAuth("ApiAuth")
        # Test with invalid username password
        self.stub_aws_srp(sa, "bad_password", "NotAuthorizedException")
        user_not_found_success = False
        try:
            sa.id_token_from_cognito(
                username="bad_password", password="wrong", client=self.aws_srp_client
            )
        except InvalidCredentialsException as e:
            self.assertIn("Please check your Secret Key is correct", e.message)
            user_not_found_success = True
        self.assertTrue(user_not_found_success)

        # Test with no access
        self.stub_aws_srp(sa, "no_access", "UserNotFoundException")
        no_access_success = False
        try:
            sa.id_token_from_cognito(
                username="no_access", password="wrong", client=self.aws_srp_client
            )
        except InvalidCredentialsException as e:
            self.assertIn(
                "Please check your Access Key, that you have created your Api Token and that you are using the right STAX REGION",
                e.message,
            )
            no_access_success = True
        self.assertTrue(no_access_success)

        # Test Unknown Error
        self.stub_aws_srp(sa, "Unknown", "UnitTesting")
        with self.assertRaises(InvalidCredentialsException):
            sa.id_token_from_cognito(
                username="Unknown", password="wrong", client=self.aws_srp_client
            )

    def testCreds(self):
        """
        Test valid credentials are returned
        """
        sa = StaxAuth("ApiAuth")
        token = jwt.encode({"sub": "unittest"}, "secret", algorithm="HS256")
        jwt_token = jwt.decode(token, verify=False)
        self.stub_cognito_creds(jwt_token.get("sub"))
        creds = sa.sts_from_cognito_identity_pool(
            jwt_token.get("sub"), self.cognito_client
        )
        self.assertIn("Credentials", creds)
        self.assertTrue(creds.get("IdentityId").startswith("ap-southeast-2"))

    def testAuthErrors(self):
        """
      Test that errors are thrown when keys are invalid
      """
        sa = StaxAuth("ApiAuth")
        # Test with no username
        with self.assertRaises(InvalidCredentialsException):
            sa.requests_auth(username=None, password="valid")

        # Test with no username
        with self.assertRaises(InvalidCredentialsException):
            sa.requests_auth(username="valid", password=None)

    def stub_aws_srp(self, stax_auth, username, error_code=None):
        expected_parameters = {
            "AuthFlow": "USER_SRP_AUTH",
            "AuthParameters": {"SRP_A": ANY, "USERNAME": username},
            "ClientId": stax_auth.client_id,
        }
        if error_code:
            self.aws_srp_stubber.add_client_error(
                "initiate_auth",
                service_error_code=error_code,
                expected_params=expected_parameters,
            )
        else:
            self.aws_srp_stubber.add_response(
                "initiate_auth",
                {
                    "ChallengeParameters": {
                        "USER_ID_FOR_SRP": "user",
                        "SALT": "4",
                        "SRP_B": "5",
                        "SECRET_BLOCK": "secblock",
                    },
                    "ChallengeName": "PASSWORD_VERIFIER",
                },
                expected_parameters,
            )
            self.aws_srp_stubber.add_response(
                "respond_to_auth_challenge",
                {"AuthenticationResult": {"IdToken": "valid_token"},},
                {
                    "ClientId": stax_auth.client_id,
                    "ChallengeName": ANY,
                    "ChallengeResponses": ANY,
                },
            )
        self.aws_srp_stubber.activate()

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
