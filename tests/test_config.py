"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import unittest
from unittest.mock import patch
import responses

from staxapp.auth import ApiTokenAuth
from staxapp.config import Config
from staxapp.exceptions import ApiException


class StaxConfigTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.Config = Config
        self.Config.init()

    @patch("staxapp.config.Config.set_config")
    def testInit(self, set_config_mock):
        """
        Test init method
        """
        self.Config._initialized = False
        test_hostname = "test.staxapp.cloud"
        self.Config.init(hostname=test_hostname)
        self.assertEqual(
            test_hostname,
            self.Config.hostname,
        )
        set_config_mock.assert_called_once()
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
            self.Config.schema_url(), f"{Config.api_base_url()}/public/api-document",
        )

    def testAuth(self):
        """
        Test auth class is returned
        """
        StaxConfig = Config
        StaxConfig.get_auth_class()
        self.assertEqual(StaxConfig.auth_class, ApiTokenAuth)


if __name__ == "__main__":
    unittest.main()
