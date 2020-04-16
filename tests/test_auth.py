"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import base64
import os
import sys
import unittest
import json
import jwt
import uuid
import boto3
import logging

from stax.auth import StaxAuth

class StaxAuthTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.access_key = os.getenv("TEST_ACCESS_KEY")
        self.secret_key = os.getenv("TEST_SECRET_KEY")
        self.assertIsNotNone(self.access_key)

    def testStaxAuthInit(self):
        sa = StaxAuth("ApiAuth")
        self.assertEqual(sa.aws_region, "ap-southeast-2")

    def testToken(self):
        """
        {'sub': 'c101dad5-2705-4678-859f-054713eb45d9', 'email_verified': True, 'iss': 'https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_QeH84DZv6', 'phone_number_verified': False, 'cognito:username': 'c101dad5-2705-4678-859f-054713eb45d9', 'cognito:roles': ['arn:aws:iam::517242832086:role/staxapiauth-stax-au1-master-cognito-ApiAdminRole-LS0VW03RNS1I'], 'aud': '3h512r2mf80ie7ld9qse0q41gq', 'event_id': 'ed4ee31e-943d-4f2f-b9a9-d45364d7618c', 'token_use': 'id', 'auth_time': 1578960699, 'name': 'baz-svc-9', 'exp': 1578964299, 'iat': 1578960699, 'email': 'QV7G0MY6UNF3NRSXLLV2FE@juma.cloud'}
        """
        sa = StaxAuth("ApiAuth")
        token = sa.id_token_from_cognito(self.access_key, self.secret_key)
        jwt_token = jwt.decode(token, verify=False)
        logging.info(f"JWT: {jwt_token}")
        self.assertIn("sub", jwt_token)

    def testCreds(self):
        """
        {'IdentityId': 'ap-southeast-2:585bdec1-a535-478e-983d-a6cee6cca9b1', 'Credentials': {'AccessKeyId': 'ASIAX000000000000000', 'SecretKey': '0000000000000000000000000000000000000000', 'SessionToken': 'a-totally-valid-JWT', 'Expiration': datetime.datetime(2020, 1, 14, 11, 52, 26, tzinfo=tzlocal())}, 'ResponseMetadata': {'RequestId': '944fdb3d-8f7c-4629-aa7a-f7b7b0df58f5', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Mon, 13 Jan 2020 23:52:26 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '1549', 'connection': 'keep-alive', 'x-amzn-requestid': '944fdb3d-8f7c-4629-aa7a-f7b7b0df58f5'}, 'RetryAttempts': 0}}
        """
        sa = StaxAuth("ApiAuth")
        token = sa.id_token_from_cognito(self.access_key, self.secret_key)
        creds = sa.sts_from_cognito_identity_pool(token)
        self.assertIn("Credentials", creds)
        self.assertTrue(creds.get("IdentityId").startswith("ap-southeast-2"))


    def testSigv4(self):
        """
        Test a simple route
        """
        pass


if __name__ == "__main__":
    unittest.main()
