"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import unittest
import responses

from staxapp.exceptions import ApiException
from staxapp.config import Config
from staxapp.api import Api


class StaxApiTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.Api = Api
        self.Api._requests_auth = lambda x, y: (x, y)
        Config.init()

    def testAuth(self):

        Config.access_key = "1"
        Config.secret_key = "2"

        auth = self.Api._auth()
        self.assertEqual(self.Api._requests_auth("1", "2"), auth)

        Config.access_key = "3"
        Config.secret_key = "4"

        auth = self.Api._auth()
        self.assertEqual(self.Api._requests_auth("3", "4"), auth)

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
            json={"Error": "Unit test failed get"},
            status=500,
        )
        with self.assertRaises(ApiException):
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
        response_dict = {"Error": "Unit Test server error for post"}
        responses.add(
            responses.POST,
            f"{Config.api_base_url()}/test/post/exception",
            json=response_dict,
            status=500,
        )
        payload = {"Unit": "Test"}
        with self.assertRaises(ApiException):
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
        with self.assertRaises(ApiException):
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
        response_dict = {"Error": "Unit test server error for put"}
        responses.add(
            responses.PUT,
            f"{Config.api_base_url()}/test/put/exception",
            json=response_dict,
            status=500,
        )
        payload = {"Unit": "Test"}
        with self.assertRaises(ApiException):
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
        with self.assertRaises(ApiException):
            self.Api.put("/test/put/400", payload)

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
        response_dict = {"Error": "Unit test server error for delete"}
        responses.add(
            responses.DELETE,
            f"{Config.api_base_url()}/test/delete/exception",
            json=response_dict,
            status=500,
        )
        with self.assertRaises(ApiException):
            self.Api.delete("/test/delete/exception")

    @responses.activate
    def testFailedApiException(self):
        """
        Test all paths of ApiException
        """
        # Test Exception with no error in response
        response_dict = {}
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/test/no/error",
            json=response_dict,
            status=500,
        )
        try:
            self.Api.get("/test/no/error")
        except ApiException as e:
            self.assertIn("Api Exception", str(e))

        # Test an exception which has no json in response
        responses.add(
            responses.GET,
            f"{Config.api_base_url()}/test/invalid/json",
            body='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>405 Method Not Allowed</title>\n<h1>Method Not Allowed</h1>\n<p>The method is not allowed for the requested URL.</p>\n',
            status=405,
        )
        with self.assertRaises(ApiException):
            self.Api.get("/test/invalid/json")

        # Test an exception with no content
        responses.add(
            responses.GET, f"{Config.api_base_url()}/test/no/content", status=500,
        )
        with self.assertRaises(ApiException):
            self.Api.get("/test/no/content")


if __name__ == "__main__":
    unittest.main()
