"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import json
import os
import unittest
from unittest.mock import patch

import pytest
import responses

from staxapp.api import Api
from staxapp.config import Config
from staxapp.exceptions import ApiException, ValidationException
from staxapp.openapi import StaxClient


class StaxClientTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.Api = Api
        self.Api._requests_auth = lambda x, y: (x, y)
        self.Config = Config()
        self.Config.init()
        self.account_client = StaxClient("accounts", config = self.Config)
        self.workload_client = StaxClient("workloads", config = self.Config)
        self.assertTrue(self.account_client._initialized)
        self.assertTrue(self.workload_client._initialized)

    def testStaxClient(self):
        """
        Test initializing Stax client
        """
        config = Config()
        self.assertFalse(config._initialized)
        client = StaxClient("accounts", config)
        self.assertTrue(client._config._initialized)

        second_client = StaxClient("accounts", config)


    def testInvalidStaxClient(self):
        """
        Test an invalid Api class raises an error
        """
        with self.assertRaises(ValidationException):
            StaxClient("fake")

    def testLoadOldSchema(self):
        """
        Test loading Old schema
        """
        StaxClient._schema = {}
        Config.load_live_schema = False
        StaxClient._load_schema()
        self.assertTrue(len(StaxClient._schema) > 0)

    def testLoadNewSchema(self):
        """
        Test loading Old schema
        """
        StaxClient._schema = {}
        Config.load_live_schema = True
        StaxClient._load_schema()
        self.assertTrue(len(StaxClient._schema) > 0)

    @patch("test_client.StaxClient._load_schema")
    def testMapOperations(self, mock_load_schema):
        """
        Test broken Map Operations
        """
        old_map = StaxClient._operation_map
        StaxClient._operation_map = {}
        StaxClient._schema = {
            "paths": {
                "Test/Route": {
                    "get": {
                        "description": "This is a test route",
                        "operationId": "Test.Route",
                        "x-stax-sdk-operation-id": "Test.Route",
                        "parameters": [],
                    }
                },
                "Test/Bad/Route": {
                    "get": {
                        "description": "This is a bad test route",
                        "operationId": "Test.Bad.Route",
                        "x-stax-sdk-operation-id": "Test.Bad.Route",
                        "parameters": [],
                    }
                }
            }
        } 
        try:
            StaxClient._map_paths_to_operations()
        except Exception as e:
            StaxClient._operation_map = old_map
            raise e

        test_map = StaxClient._operation_map
        StaxClient._operation_map = old_map
        self.assertEqual(test_map, {'Test': {'Route': [{'path': 'Test/Route', 'method': 'get', 'parameters': []}]}})

    @responses.activate
    @patch("test_client.Config._auth")
    def testStaxWrapper(self, staxclient_auth_mock):
        """
        Test the Stax client wrapper
        """
        # Test a valid GET
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{self.Config.api_base_url()}/accounts",
            json=response_dict,
            status=200,
        )
        response = self.account_client.ReadAccounts()
        self.assertEqual(response, response_dict)

        # Test a valid GET with path params
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{self.Config.api_base_url()}/accounts/fake-id",
            json=response_dict,
            status=200,
        )
        params = {"account_id": "fake-id", "Unit": "Test"}
        response = self.account_client.ReadAccounts(**params)
        self.assertEqual(response, response_dict)

        # Test a valid GET with params
        response_dict = {"Status": "OK"}
        responses.add(
            responses.GET,
            f"{self.Config.api_base_url()}/accounts",
            json=response_dict,
            status=200,
        )
        params = {"Unit": "Test"}
        response = self.account_client.ReadAccounts(**params)
        self.assertEqual(response, response_dict)

        # Test a valid POST
        response_dict = {"Status": "OK"}
        responses.add(
            responses.POST,
            f"{self.Config.api_base_url()}/accounts",
            json=response_dict,
            status=200,
        )
        response = self.account_client.CreateAccount(Name="Unit", AccountType="ab13a455-033f-4947-8393-641eefc3ba5e")
        self.assertEqual(response, response_dict)


    @responses.activate
    @patch("test_client.Config._auth")
    def testStaxWrapperErrors(self, staxclient_auth_mock):
        """
        Test raising errors in StaxWrapper
        """

        # To ensure it fails on the assertion not calling the response
        response_dict = {"Error": "A unique UnitTest error for workload catalogues"}
        responses.add(
            responses.GET,
            f"{self.Config.api_base_url()}/workload-catalogue/fake-id/fake-id",
            json=response_dict,
            status=400,
        )
        # Test an error occurs when the wrong client is used
        with self.assertRaises(ValidationException):
            self.account_client.ReadCatalogueVersion(
                catalogue_id="fake-id", version_id="fake-id", force=True
            )
        # Test an error occurs when a parameter is missing
        with self.assertRaises(ValidationException):
            self.workload_client.ReadCatalogueVersion(version_id="fake-id/fake-id", force=True)
        # Test an error occurs when error in response
        with self.assertRaises(ApiException):
            self.workload_client.ReadCatalogueVersion(
                catalogue_id="fake-id", version_id="fake-id", force=True
            )


class TestStaxClientOperations:
    @pytest.fixture(autouse=True)
    @patch("staxapp.openapi.StaxClient._load_schema")
    def setup_class(self, _):
        def get_operation_map(schema_path, use_custom_operation_ids):
            preexisting_operation_map = {**StaxClient._operation_map}
            StaxClient._operation_map = {}
            
            with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), schema_path), "r") as f:
                schema = json.loads(f.read())
            
            StaxClient._schema = schema
            # The new schema uses x-stax-sdk-operation-id, as ordinarily OpenAPI expects a unique operationId for 
            # every path and method; to try and preserve behaviour in previous versions of the SDK we must derive
            # operations from the x-stax-sdk-operation-id field instead of the operationId field.
            # _use_custom_operation_ids is only to be used for testing purposes.
            StaxClient._use_custom_operation_ids = use_custom_operation_ids
            StaxClient._map_paths_to_operations()
            operation_map = {**StaxClient._operation_map}

            StaxClient._operation_map = {**preexisting_operation_map}
            
            return operation_map

        self.old_operation_map = get_operation_map(schema_path="data/old_schema.json", use_custom_operation_ids=False)
        self.new_operation_map = get_operation_map(schema_path="../staxapp/data/schema.json", use_custom_operation_ids=True)


    @patch("staxapp.api.Api.post")
    @patch("staxapp.api.Api.get")
    @pytest.mark.parametrize("client_name,operation,operation_args", [
        ("accounts", "DiscoverAccounts", {}),
        ("accounts", "DiscoverAccounts", {"aws_account_id": "test"}),
        ("accounts", "ReadAccounts", {}),
        ("accounts", "ReadAccounts", {"account_id": "test"}),
        ("accounts", "ReadAccountTypes", {}),
        ("accounts", "ReadAccountTypes", {"account_type_id": "test"}),
        ("networking", "ReadCidrExclusions", {}),
        ("networking", "ReadCidrExclusions", {"exclusion_id": "test"}),
        ("networking", "ReadCidrExclusions", {"hub_id": "test"}),
        ("networking", "ReadCidrRanges", {}),
        ("networking", "ReadCidrRanges", {"hub_id": "test"}),
        ("networking", "ReadCidrRanges", {"range_id": "test"}),
        ("networking", "ReadDnsResolvers", {}),
        ("networking", "ReadDnsResolvers", {"dns_resolver_id": "test"}),
        ("networking", "ReadDnsResolvers", {"hub_id": "test"}),
        ("networking", "ReadDnsRules", {}),
        ("networking", "ReadDnsRules", {"dns_resolver_id": "test"}),
        ("networking", "ReadDnsRules", {"dns_rule_id": "test"}),
        ("networking", "ReadDxAssociations", {}),
        ("networking", "ReadDxAssociations", {"dx_association_id": "test"}),
        ("networking", "ReadDxAssociations", {"dx_gateway_id": "test"}),
        ("networking", "ReadDxAssociations", {"hub_id": "test"}),
        ("networking", "ReadDxGateways", {}),
        ("networking", "ReadDxGateways", {"dx_gateway_id": "test"}),
        ("networking", "ReadDxGateways", {"hub_id": "test"}),
        ("networking", "ReadDxVifs", {}),
        ("networking", "ReadDxVifs", {"dx_vif_id": "test"}),
        ("networking", "ReadDxVifs", {"dx_gateway_id": "test"}),
        ("networking", "ReadHubs", {}),
        ("networking", "ReadHubs", {"hub_id": "test"}),
        ("networking", "ReadVpcs", {}),
        ("networking", "ReadVpcs", {"hub_id": "test"}),
        ("networking", "ReadVpcs", {"vpc_id": "test"}),
        ("networking", "ReadVpnConnections", {}),
        ("networking", "ReadVpnConnections", {"hub_id": "test"}),
        ("networking", "ReadVpnConnections", {"vpn_connection_id": "test"}),
        ("networking", "ReadVpnConnections", {"vpn_customer_gateway_id": "test"}),
        ("networking", "ReadVpnCustomerGateways", {}),
        ("networking", "ReadVpnCustomerGateways", {"hub_id": "test"}),
        ("networking", "ReadVpnCustomerGateways", {"vpn_customer_gateway_id": "test"}),
        ("organisations", "ReadPolicies", {}),
        ("organisations", "ReadPolicies", {"policy_id": "test"}),
        ("teams", "ReadApiTokens", {}),
        ("teams", "ReadApiTokens", {"access_key": "test"}),
        ("teams", "ReadGroups", {}),
        ("teams", "ReadGroups", {"group_id": "test"}),
        ("teams", "ReadUsers", {}),
        ("teams", "ReadUsers", {"user_id": "test"}),
        ("workloads", "ReadCatalogueItems", {}),
        ("workloads", "ReadCatalogueItems", {"catalogue_id": "test"}),
        ("workloads", "ReadWorkloads", {}),
        ("workloads", "ReadWorkloads", {"workload_id": "test"}),
    ])
    def test_operation_overload_routes_to_correct_path(self, mock_api_get, mock_api_post, client_name, operation, operation_args):
        # Although there should be virtually no difference between the old and new schema regarding parameters, 
        # ReadApiTokens has a parameter named AccessKey, which is unusual considering most other parameters being 
        # snakecased, which the new schema would have fixed. Regardless of casing, we'd still like to know if the 
        # operation routes to the correct path.
        old_operation_args = {
            (
                "AccessKey"
                if k == "access_key"
                and client_name == "teams"
                and operation == "ReadApiTokens"
                else k
            ): v
            for k, v in operation_args.items()
        }

        # Find the definition of the operation for the purposes of deriving the method, to be used in retrieving
        # the correct API request mock.
        matching_operation_definition = next(
            (
                x
                for x in self.old_operation_map[client_name][operation]
                if {*old_operation_args} == {*x["parameters"]}
            ),
            {},
        )

        mocked_request_method = {
            "get": mock_api_get,
            "post": mock_api_post,
        }.get(matching_operation_definition["method"])

        StaxClient._operation_map = {**self.old_operation_map}
        assert StaxClient._operation_map != self.new_operation_map

        client = StaxClient(client_name, config=Config())
        getattr(client, operation)(**old_operation_args)
        old_path, old_payload, _cfg = mocked_request_method.call_args.args

        mocked_request_method.reset_mock()

        StaxClient._operation_map = {**self.new_operation_map}
        assert StaxClient._operation_map != self.old_operation_map
        getattr(client, operation)(**operation_args)
        new_path, new_payload, _cfg = mocked_request_method.call_args.args

        assert new_path == old_path
        assert new_payload == old_payload

if __name__ == "__main__":
    unittest.main()
