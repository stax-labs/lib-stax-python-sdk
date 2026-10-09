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
        self.account_client = StaxClient("accounts", config=self.Config)
        self.workload_client = StaxClient("workloads", config=self.Config)
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
                },
            }
        }
        try:
            StaxClient._map_paths_to_operations()
        except Exception as e:
            StaxClient._operation_map = old_map
            raise e

        test_map = StaxClient._operation_map
        StaxClient._operation_map = old_map
        self.assertEqual(
            test_map,
            {
                "Test": {
                    "Route": [{"path": "Test/Route", "method": "get", "parameters": []}]
                }
            },
        )

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
        response = self.account_client.CreateAccount(
            Name="Unit", AccountType="ab13a455-033f-4947-8393-641eefc3ba5e"
        )
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
            self.workload_client.ReadCatalogueVersion(
                version_id="fake-id/fake-id", force=True
            )
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

            with open(
                os.path.join(os.path.abspath(os.path.dirname(__file__)), schema_path),
                "r",
            ) as f:
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

        self.old_operation_map = get_operation_map(
            schema_path="data/old_schema.json", use_custom_operation_ids=False
        )
        self.new_operation_map = get_operation_map(
            schema_path="../staxapp/data/schema.json", use_custom_operation_ids=True
        )

    @patch("staxapp.api.Api.delete")
    @patch("staxapp.api.Api.put")
    @patch("staxapp.api.Api.post")
    @patch("staxapp.api.Api.get")
    @pytest.mark.parametrize(
        "client_name,operation,operation_args,request_body",
        [
            ("accounts", "UpdateAccountTypeMembers", {}, {"Members": []}),
            ("accounts", "ReadAccounts", {}, {}),
            ("accounts", "CreateAccount", {}, {"Name": "test", "AccountType": "test"}),
            (
                "accounts",
                "CloseAccount",
                {},
                {"Id": "00000000-0000-0000-0000-000000000000"},
            ),
            ("accounts", "DiscoverAccounts", {}, {}),
            ("accounts", "DiscoverAccounts", {"aws_account_id": "test"}, {}),
            (
                "accounts",
                "OnboardAccount",
                {},
                {"AwsAccountId": "000000000000", "AccountType": "test"},
            ),
            ("accounts", "ReadAccountTypes", {}, {}),
            ("accounts", "CreateAccountType", {}, {"Name": "test"}),
            ("accounts", "UpdateAccountTypeAccess", {}, {}),
            ("accounts", "DeleteAccountType", {"account_type_id": "test"}, {}),
            ("accounts", "ReadAccountTypes", {"account_type_id": "test"}, {}),
            (
                "accounts",
                "UpdateAccountType",
                {"account_type_id": "test"},
                {"Name": "test"},
            ),
            ("accounts", "ReadAccounts", {"account_id": "test"}, {}),
            ("accounts", "UpdateAccount", {"account_id": "test"}, {}),
            ("accounts", "ReadAccountPolicyAttachments", {"account_id": "test"}, {}),
            ("teams", "ReadApiTokens", {}, {}),
            ("teams", "CreateApiToken", {}, {"Name": "test", "Role": "api_readonly"}),
            ("teams", "DeleteApiToken", {"access_key": "test"}, {}),
            ("teams", "ReadApiTokens", {"access_key": "test"}, {}),
            ("teams", "UpdateApiToken", {"access_key": "test"}, {}),
            ("teams", "ReadGroups", {}, {}),
            ("teams", "CreateGroup", {}, {"Name": "test"}),
            ("teams", "UpdateGroupMembers", {}, {}),
            ("teams", "DeleteGroup", {"group_id": "test"}, {}),
            ("teams", "ReadGroups", {"group_id": "test"}, {}),
            ("teams", "UpdateGroup", {"group_id": "test"}, {"Name": "test"}),
            (
                "teams",
                "CreateUser",
                {},
                {"FirstName": "test", "LastName": "test", "Email": "test@test.test"},
            ),
            ("teams", "UpdateUserInvite", {"user_id": "test"}, {}),
            ("teams", "UpdateUserPassword", {"user_id": "test"}, {}),
            ("teams", "UpdateUser", {"user_id": "test"}, {}),
            ("insights", "ReadInsights", {}, {}),
            ("networking", "ReadDnsResolvers", {}, {}),
            ("networking", "DeleteDnsResolver", {"dns_resolver_id": "test"}, {}),
            ("networking", "ReadDnsResolvers", {"dns_resolver_id": "test"}, {}),
            ("networking", "UpdateDnsResolver", {"dns_resolver_id": "test"}, {}),
            ("networking", "ReadDnsRules", {"dns_resolver_id": "test"}, {}),
            (
                "networking",
                "CreateDnsRule",
                {"dns_resolver_id": "test"},
                {"Name": "test", "DomainName": "test.test", "ForwarderIpAddresses": []},
            ),
            ("networking", "ReadDnsRules", {}, {}),
            ("networking", "DeleteDnsRule", {"dns_rule_id": "test"}, {}),
            ("networking", "ReadDnsRules", {"dns_rule_id": "test"}, {}),
            ("networking", "UpdateDnsRule", {"dns_rule_id": "test"}, {}),
            ("networking", "ReadDxAssociations", {}, {}),
            ("networking", "DeleteDxAssociation", {"dx_association_id": "test"}, {}),
            ("networking", "UpdateDxAssociation", {"dx_association_id": "test"}, {}),
            ("networking", "ReadDxGateways", {}, {}),
            ("networking", "DeleteDxGateway", {"dx_gateway_id": "test"}, {}),
            ("networking", "ReadDxGateways", {"dx_gateway_id": "test"}, {}),
            ("networking", "ReadDxAssociations", {"dx_gateway_id": "test"}, {}),
            (
                "networking",
                "CreateDxAssociation",
                {"dx_gateway_id": "test"},
                {
                    "NetworkingHubId": "00000000-0000-0000-0000-000000000000",
                    "Prefixes": [],
                },
            ),
            ("networking", "ReadDxVifs", {"dx_gateway_id": "test"}, {}),
            ("networking", "CreateDxResource", {}, {}),
            ("networking", "ReadDxVifs", {}, {}),
            ("networking", "DeleteDxVif", {"dx_vif_id": "test"}, {}),
            ("networking", "ReadDxVifs", {"dx_vif_id": "test"}, {}),
            ("networking", "UpdateDxVif", {"dx_vif_id": "test"}, {}),
            ("networking", "ReadDxVifStatus", {"dx_vif_id": "test"}, {}),
            ("networking", "ReadCidrExclusions", {}, {}),
            ("networking", "DeleteCidrExclusion", {"exclusion_id": "test"}, {}),
            ("networking", "ReadCidrExclusions", {"exclusion_id": "test"}, {}),
            ("networking", "UpdateCidrExclusion", {"exclusion_id": "test"}, {}),
            ("networking", "ReadHubPeerings", {}, {}),
            ("networking", "DeleteHubPeering", {"hub_peering_id": "test"}, {}),
            ("networking", "ReadHubPeering", {"hub_peering_id": "test"}, {}),
            ("networking", "UpdateHubPeering", {"hub_peering_id": "test"}, {}),
            ("networking", "ReadHubs", {}, {}),
            (
                "networking",
                "CreateHub",
                {},
                {
                    "Name": "test",
                    "AccountId": "00000000-0000-0000-0000-000000000000",
                    "Region": "us-east-1",
                    "Cidr": "test",
                    "CreateNatGateway": True,
                    "CreateInternetGateway": True,
                },
            ),
            ("networking", "DeleteHub", {"hub_id": "test"}, {}),
            ("networking", "ReadHubs", {"hub_id": "test"}, {}),
            ("networking", "UpdateHub", {"hub_id": "test"}, {}),
            ("networking", "ReadDnsResolvers", {"hub_id": "test"}, {}),
            (
                "networking",
                "CreateDnsResolver",
                {"hub_id": "test"},
                {"Name": "test", "NumberOfInterfaces": 2},
            ),
            ("networking", "ReadDxAssociations", {"hub_id": "test"}, {}),
            ("networking", "ReadDxGateways", {"hub_id": "test"}, {}),
            ("networking", "ReadCidrExclusions", {"hub_id": "test"}, {}),
            (
                "networking",
                "CreateCidrExclusion",
                {"hub_id": "test"},
                {"Name": "test", "Cidr": "test"},
            ),
            ("networking", "ReadHubPrefixLists", {"hub_id": "test"}, {}),
            (
                "networking",
                "CreateHubPrefixList",
                {"hub_id": "test"},
                {"Name": "test", "MaxEntries": 3, "Entries": [], "TargetType": "VPN"},
            ),
            (
                "networking",
                "CreateVpcPrefixList",
                {"hub_id": "test"},
                {"Name": "test", "MaxEntries": 3, "Entries": []},
            ),
            ("networking", "ReadCidrRanges", {"hub_id": "test"}, {}),
            (
                "networking",
                "CreateCidrRange",
                {"hub_id": "test"},
                {"Name": "test", "Cidr": "test"},
            ),
            ("networking", "ReadVpcs", {"hub_id": "test"}, {}),
            (
                "networking",
                "CreateVpc",
                {"hub_id": "test"},
                {
                    "Name": "test",
                    "CidrRangeId": "00000000-0000-0000-0000-000000000000",
                    "AccountId": "00000000-0000-0000-0000-000000000000",
                    "Region": "us-east-1",
                    "Size": "SMALL",
                    "Type": "FLAT",
                    "CreateInternetGateway": True,
                },
            ),
            ("networking", "ReadVpnConnections", {"hub_id": "test"}, {}),
            ("networking", "ReadVpnCustomerGateways", {"hub_id": "test"}, {}),
            ("networking", "ReadHubHubPeerings", {"networking_hub_id": "test"}, {}),
            (
                "networking",
                "CreateHubPeering",
                {"networking_hub_id": "test"},
                {"Name": "test", "HubPeeringTarget": "STAX_RESOURCE"},
            ),
            ("networking", "ReadPrefixLists", {}, {}),
            (
                "networking",
                "UpdateHubPrefixListAssociation",
                {"prefix_list_id": "test"},
                {},
            ),
            (
                "networking",
                "UpdateVpcPrefixListAssociation",
                {"prefix_list_id": "test"},
                {},
            ),
            ("networking", "DeletePrefixList", {"prefix_list_id": "test"}, {}),
            ("networking", "ReadPrefixList", {"prefix_list_id": "test"}, {}),
            ("networking", "UpdatePrefixList", {"prefix_list_id": "test"}, {}),
            ("networking", "ReadCidrRanges", {}, {}),
            ("networking", "DeleteCidrRange", {"range_id": "test"}, {}),
            ("networking", "ReadCidrRanges", {"range_id": "test"}, {}),
            ("networking", "UpdateCidrRange", {"range_id": "test"}, {}),
            ("networking", "ReadVpcs", {}, {}),
            ("networking", "DeleteVpc", {"vpc_id": "test"}, {}),
            ("networking", "ReadVpcs", {"vpc_id": "test"}, {}),
            ("networking", "UpdateVpc", {"vpc_id": "test"}, {}),
            ("networking", "ReadVpnConnections", {}, {}),
            ("networking", "DeleteVpnConnection", {"vpn_connection_id": "test"}, {}),
            ("networking", "ReadVpnConnections", {"vpn_connection_id": "test"}, {}),
            ("networking", "UpdateVpnConnection", {"vpn_connection_id": "test"}, {}),
            (
                "networking",
                "ReadVpnConnectionStatus",
                {"vpn_connection_id": "test"},
                {},
            ),
            ("networking", "ReadVpnCustomerGateways", {}, {}),
            (
                "networking",
                "CreateVpnCustomerGateway",
                {},
                {
                    "Name": "test",
                    "Asn": 64513,
                    "IpAddress": "0.0.0.0",
                    "AccountId": "00000000-0000-0000-0000-000000000000",
                    "Region": "us-east-1",
                },
            ),
            (
                "networking",
                "DeleteVpnCustomerGateway",
                {"vpn_customer_gateway_id": "test"},
                {},
            ),
            (
                "networking",
                "ReadVpnCustomerGateways",
                {"vpn_customer_gateway_id": "test"},
                {},
            ),
            (
                "networking",
                "UpdateVpnCustomerGateway",
                {"vpn_customer_gateway_id": "test"},
                {},
            ),
            (
                "networking",
                "CreateVpnConnection",
                {"vpn_customer_gateway_id": "test"},
                {"Name": "test", "VpcId": "00000000-0000-0000-0000-000000000000"},
            ),
            (
                "networking",
                "ReadVpnConnections",
                {"vpn_customer_gateway_id": "test"},
                {},
            ),
            ("networking", "ReadDxConnections", {"account_id": "test"}, {}),
            ("organisations", "ReadOrganisations", {}, {}),
            ("organisations", "ReadOrganisation", {}, {}),
            ("organisations", "ReadOrganizationFeatures", {}, {}),
            ("organisations", "ReadOrganisationalUnits", {}, {}),
            (
                "organisations",
                "CreateOrganisationalUnit",
                {},
                {
                    "Name": "test",
                    "ParentOrganisationalUnitId": "00000000-0000-0000-0000-000000000000",
                },
            ),
            (
                "organisations",
                "DeleteOrganisationalUnit",
                {"organisational_unit_id": "test"},
                {},
            ),
            (
                "organisations",
                "ReadOrganisationalUnit",
                {"organisational_unit_id": "test"},
                {},
            ),
            (
                "organisations",
                "UpdateOrganisationalUnit",
                {"organisational_unit_id": "test"},
                {},
            ),
            (
                "organisations",
                "ReadOrganisationalUnitAccounts",
                {"organisational_unit_id": "test"},
                {},
            ),
            (
                "organisations",
                "ReadOrganisationalUnitPolicyAttachments",
                {"organisational_unit_id": "test"},
                {},
            ),
            ("organisations", "ReadPolicies", {}, {}),
            (
                "organisations",
                "CreatePolicy",
                {},
                {"Name": "test", "Description": "test", "Policy": "test"},
            ),
            ("policies", "DetachPolicy", {"policy_attachment_id": "test"}, {}),
            ("organisations", "DetachPolicy", {"policy_id": "test"}, {}),
            ("organisations", "AttachPolicy", {"policy_id": "test"}, {}),
            ("organisations", "DeletePolicy", {"policy_id": "test"}, {}),
            ("organisations", "ReadPolicies", {"policy_id": "test"}, {}),
            ("organisations", "UpdatePolicy", {"policy_id": "test"}, {}),
            ("policies", "ReadPolicyAttachments", {"policy_id": "test"}, {}),
            (
                "policies",
                "AttachPolicy",
                {"policy_id": "test"},
                {"AccountId": "00000000-0000-0000-0000-000000000000"},
            ),
            ("public", "CheckAlias", {"alias": "test"}, {}),
            ("public", "ReadConfig", {}, {}),
            ("services", "ReadAccountConfiguration", {}, {}),
            ("services", "ReadGuardDutyConfiguration", {}, {}),
            ("services", "ReadGuardrailsConfiguration", {}, {}),
            ("services", "ReadOrganizationConfiguration", {}, {}),
            ("services", "ReadRegionsConfiguration", {}, {}),
            ("services", "ReadSecurityHubConfiguration", {}, {}),
            ("services", "ReadSsoConfiguration", {}, {}),
            ("tasks", "ReadTask", {"task_id": "test"}, {}),
            ("teams", "ReadUsers", {}, {}),
            ("teams", "FetchCurrentUser", {}, {}),
            ("teams", "DeleteUser", {"user_id": "test"}, {}),
            ("teams", "ReadUsers", {"user_id": "test"}, {}),
            ("workloads", "ReadCatalogueItems", {}, {}),
            (
                "workloads",
                "CreateCatalogueItem",
                {},
                {"Name": "test", "Version": "test", "Description": "test"},
            ),
            ("workloads", "ReadCatalogueManifest", {"version_id": "test"}, {}),
            (
                "workloads",
                "ReadCatalogueTemplate",
                {"version_id": "test", "name": "test"},
                {},
            ),
            ("workloads", "DeleteCatalogueItem", {"catalogue_id": "test"}, {}),
            ("workloads", "ReadCatalogueItems", {"catalogue_id": "test"}, {}),
            (
                "workloads",
                "CreateCatalogueVersion",
                {"catalogue_id": "test"},
                {"Version": "test", "Description": "test"},
            ),
            (
                "workloads",
                "DeleteCatalogueVersion",
                {"catalogue_id": "test", "version_id": "test"},
                {},
            ),
            (
                "workloads",
                "ReadCatalogueVersion",
                {"catalogue_id": "test", "version_id": "test"},
                {},
            ),
            ("workloads", "ReadWorkloads", {}, {}),
            (
                "workloads",
                "CreateWorkload",
                {},
                {
                    "Name": "test",
                    "CatalogueId": "00000000-0000-0000-0000-000000000000",
                    "AccountId": "00000000-0000-0000-0000-000000000000",
                    "Region": "us-east-1",
                },
            ),
            ("workloads", "DeleteWorkload", {"workload_id": "test"}, {}),
            ("workloads", "ReadWorkloads", {"workload_id": "test"}, {}),
            ("workloads", "UpdateWorkload", {"workload_id": "test"}, {}),
        ],
    )
    def test_operation_overload_routes_to_correct_path(
        self,
        mock_api_get,
        mock_api_post,
        mock_api_put,
        mock_api_delete,
        client_name,
        operation,
        operation_args,
        request_body,
    ):
        # Although there should be virtually no difference between the old and new schema regarding parameters,
        # ReadApiTokens has a parameter named AccessKey, which is unusual considering most other parameters being
        # snakecased, which the new schema would have fixed. Regardless of casing, we'd still like to know if the
        # operation routes to the correct path.
        old_operation_args = {
            (
                "AccessKey"
                if k == "access_key"
                and client_name == "teams"
                and operation in ["ReadApiTokens", "UpdateApiToken", "DeleteApiToken"]
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
            "put": mock_api_put,
            "delete": mock_api_delete,
        }.get(matching_operation_definition["method"])

        StaxClient._operation_map = {**self.old_operation_map}
        assert StaxClient._operation_map != self.new_operation_map

        client = StaxClient(client_name, config=Config())

        with patch("staxapp.contract.StaxContract.validate"):
            getattr(client, operation)(**old_operation_args, **request_body)
            old_path, old_payload, _cfg = mocked_request_method.call_args.args

        mocked_request_method.reset_mock()

        StaxClient._operation_map = {**self.new_operation_map}
        assert StaxClient._operation_map != self.old_operation_map
        getattr(client, operation)(**operation_args, **request_body)
        new_path, new_payload, _cfg = mocked_request_method.call_args.args

        assert new_path == old_path
        assert new_payload == old_payload


if __name__ == "__main__":
    unittest.main()
