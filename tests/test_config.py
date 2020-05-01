"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import os
import unittest

from stax.config import Config
from stax.auth import ApiTokenAuth


class StaxConfigTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

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
            f"https://api.{self.Config.STAX_REGION}/{self.Config.API_VERSION}/public/api-document",
        )
        # Test feature branch
        os.environ["BRANCH"] = "unittest"
        self.assertEqual(
            self.Config.schema_url(),
            f"https://api-{self.Config.branch()}.{self.Config.STAX_REGION}/{self.Config.API_VERSION}/public/api-document",
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
