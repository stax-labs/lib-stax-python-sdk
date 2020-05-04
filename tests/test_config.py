"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import os
import unittest
import responses
import requests

from stax.auth import ApiTokenAuth
from stax.config import Config
from stax.exceptions import ApiException

class StaxConfigTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """
    def setUp(self):
        self.Config = Config
        self.Config.init()
        self.assertTrue(self.Config._initialized)

    @responses.activate
    def testConfigError(self):
        response_dict = {"Error": "Unittest"}
        responses.add(
            responses.GET,
            f"https://api.au1.staxapp.cloud/20190206/public/config",
            json=response_dict,
            status=500,
        )
        self.Config._initialized = False
        with self.assertRaises(ApiException):
            self.Config.init()
       

    def testConfig(self):
        """
        Test config class variables are accessible
        """
        self.assertEqual(self.Config.STAX_REGION, "au1.staxapp.cloud")
        self.assertEqual(self.Config.API_VERSION, "20190206")
    
    def testBaseUrl(self):
        """
        Test base url is returned
        """
        self.Config.api_base_url()
        self.assertTrue(self.Config.base_url)

    def testBranch(self):
        """
        Test branch is returned
        """
        self.assertEqual(self.Config.branch(), "master")

    def testSchemaUrl(self):
        """
        Test schema url is returned
        """
        self.assertEqual(
            self.Config.schema_url(),
            f"{Config.api_base_url()}/public/api-document",
        )

    def testAuth(self):
        """
        Test auth class is returned
        """
        self.Config.auth()
        self.assertEqual(self.Config.auth_class, ApiTokenAuth)


if __name__ == "__main__":
    unittest.main()
