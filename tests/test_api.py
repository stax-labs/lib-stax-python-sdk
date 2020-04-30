"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import unittest
import responses
import requests

from requests.exceptions import HTTPError

from stax.config import Config
from stax.api import Api


class StaxApiTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.Api = Api
        self.Api._requests_auth = ("username", "password")

    def testAuth(self):
        auth = self.Api._auth()
        self.assertEqual(self.Api._requests_auth, auth)

    @responses.activate
    def testGet(self):
        """
        Test GET route
        """
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/test/get/200",
            json=response_dict,
            status=200,
        )
        response = self.Api.get("/test/get/200")
        self.assertEqual(response, response_dict)

    @responses.activate
    def testGetWithParams(self):
        """
        Test GET with parameters
        """
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/test/get/200",
            json=response_dict,
            status=200,
        )
        params = {"test_param": "unit"}
        response = self.Api.get("/test/get/200", params)
        self.assertEqual(response, response_dict)

    @responses.activate
    def testFailedGet(self):
        """
        Test failed GET route
        """
        # Test HTTP exception
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/test/get/exception",
            HTTPError("Failed GET"),
        )
        with self.assertRaises(requests.exceptions.HTTPError):
            self.Api.get("/test/get/exception")

    @responses.activate
    def testPost(self):
        """
        Test POST route
        """
        response_dict = {"Status": "OK"}
        responses.add(
            responses.POST,
            f"{Config.api_base_url()}/test/post/200",
            json=response_dict,
            status=200,
        )
        payload = {"Unit": "Test"}
        response = self.Api.post("/test/post/200", payload)
        self.assertEqual(response, response_dict)

    @responses.activate
    def testFailedPost(self):
        """
        Test failed POST route
        """
        # Test HTTP exception
        responses.add(
            responses.POST,
            f"{Config.api_base_url()}/test/post/exception",
            HTTPError("Failed POST"),
        )
        payload = {"Unit": "Test"}
        with self.assertRaises(requests.exceptions.HTTPError):
            self.Api.post("/test/post/exception", payload)

        # Test 400 response
        response_dict = {"Status": "FAILED"}
        responses.add(
            responses.POST,
            f"{Config.api_base_url()}/test/post/400",
            json=response_dict,
            status=400,
        )
        payload = {"Unit": "Test"}
        response = self.Api.post("/test/post/400", payload)
        self.assertEqual(response, response_dict)

    @responses.activate
    def testPut(self):
        """
        Test PUT route
        """
        response_dict = {"Status": "OK"}
        responses.add(
            responses.PUT,
            f"{Config.api_base_url()}/test/put/200",
            json=response_dict,
            status=200,
        )
        payload = {"Unit": "Test"}
        response = self.Api.put("/test/put/200", payload)
        self.assertEqual(response, response_dict)

    @responses.activate
    def testFailedPut(self):
        """
        Test failed PUT route
        """
        # Test HTTP exception
        responses.add(
            responses.PUT,
            f"{Config.api_base_url()}/test/put/exception",
            HTTPError("Failed PUT"),
        )
        payload = {"Unit": "Test"}
        with self.assertRaises(requests.exceptions.HTTPError):
            self.Api.put("/test/put/exception", payload)

        # Test 400 response
        response_dict = {"Status": "FAILED"}
        responses.add(
            responses.PUT,
            f"{Config.api_base_url()}/test/put/400",
            json=response_dict,
            status=400,
        )
        payload = {"Unit": "Test"}
        response = self.Api.put("/test/put/400", payload)
        self.assertEqual(response, response_dict)

    @responses.activate
    def testDelete(self):
        """
        Test DELETE route
        """
        response_dict = {"Status": "OK"}
        responses.add(
            responses.DELETE,
            f"{Config.api_base_url()}/test/delete/200",
            json=response_dict,
            status=200,
        )
        response = self.Api.delete("/test/delete/200")
        self.assertEqual(response, response_dict)

    @responses.activate
    def testFailedDelete(self):
        """
        Test failed DELETE route
        """
        # Test HTTP exception
        responses.add(
            responses.DELETE,
            f"{Config.api_base_url()}/test/delete/exception",
            HTTPError("Failed DELETE"),
        )
        with self.assertRaises(requests.exceptions.HTTPError):
            self.Api.delete("/test/delete/exception")


if __name__ == "__main__":
    unittest.main()
