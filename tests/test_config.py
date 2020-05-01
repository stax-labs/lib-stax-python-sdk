"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import os
import unittest
import responses
import requests

from stax.config import Config
from stax.auth import ApiTokenAuth


class StaxConfigTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """
    os.environ["API_VERSION"] = "20190206"
    os.environ["STAX_BRANCH"] = "master"


    def setUp(self):
        self.Config = Config
        self.assertTrue(self.Config._initialized)

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
        # Test master branch
        self.assertEqual(
            self.Config.schema_url(),
            f"{Config.api_base_url()}/public/api-document",
        )

    @responses.activate
    def testFeatureBranch(self):
        # Test feature branch
        os.environ["STAX_BRANCH"] = "unittest"
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"https://api.dev-unittest.{self.Config.STAX_REGION}/{self.Config.API_VERSION}/public/config",
            json=response_dict,
            status=200,
        )
        self.Config._initialized = False
        self.Config.init()
        self.assertEqual(
            self.Config.schema_url(),
            f"https://api.dev-unittest.{self.Config.STAX_REGION}/{self.Config.API_VERSION}/public/api-document",
        )
        del os.environ["BRANCH"]

    def testAuth(self):
        """
        Test auth class is returned
        """
        self.Config.auth()
        self.assertEqual(self.Config.auth_class, ApiTokenAuth)


if __name__ == "__main__":
    unittest.main()
