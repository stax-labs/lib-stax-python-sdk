"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import responses
import unittest

from stax.api import Api
from stax.config import Config
from stax.openapi import StaxClient


class StaxClientTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.Api = Api
        self.Api._requests_auth = ("username", "password")

        self.client = StaxClient("accounts")
        self.assertTrue(self.client._initialized)

    def testStaxClient(self):
        """
        Test initializing Stax client
        """
        client = StaxClient("accounts", lambda_client=True)
        self.assertTrue(client._initialized)
        self.assertTrue(client._admin)

    def testLoadLiveSchema(self):
        """
        Test loading live schema
        """
        self.Config = Config
        self.Config.load_live_schema = True
        client = StaxClient("accounts")
        self.assertTrue(client._initialized)

    @responses.activate
    def testStaxWrapper(self):
        """
        Test the Stax client wrapper
        """
        # Test a valid GET
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/accounts",
            json=response_dict,
            status=200,
        )
        response = self.client.ReadAccounts()
        self.assertEqual(response, response_dict)

        # Test a valid GET with path params
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/accounts/fake-id",
            json=response_dict,
            status=200,
        )
        params = {"account_id": "fake-id", "Unit": "Test"}
        response = self.client.ReadAccounts(**params)
        self.assertEqual(response, response_dict)

                # Test a valid GET with params
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/accounts",
            json=response_dict,
            status=200,
        )
        params = {"Unit": "Test"}
        response = self.client.ReadAccounts(**params)
        self.assertEqual(response, response_dict)

        # Test a valid POST
        response_dict = {"Status": "OK"}
        responses.add(
            responses.POST,
            f"{Config.api_base_url()}/accounts",
            json=response_dict,
            status=200,
        )
        response = self.client.CreateAccount(Name="Unit", AccountType="Test")
        self.assertEqual(response, response_dict)


if __name__ == "__main__":
    unittest.main()
