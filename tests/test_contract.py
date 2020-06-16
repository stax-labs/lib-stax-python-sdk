"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import unittest

from staxapp.contract import StaxContract
from staxapp.exceptions import ValidationException


class StaxContractTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        self.StaxContract = StaxContract

    def testInvalidSchema(self):
        """
        Test an error is thrown if no schema is found
        """
        sc = StaxContract
        sc._swagger_doc = None
        data = {"Name": "Unit", "AccountType": "Test"}
        component = "accounts.CreateAccount"
        sc.validate(data, component)
        self.assertIsNotNone(sc._swagger_doc)

    def testDefaultSchema(self):
        """
        Test the default schema is valid
        """
        schema = self.StaxContract.default_swagger_template()
        self.assertEqual(schema.get("info").get("title"), "Stax Core API")
        self.assertIsInstance(schema.get("components").get("schemas"), dict)

    def testGetSchema(self):
        """
        Test getting the default schema
        """
        data = {"Name": "Unit", "AccountType": "ab13a455-033f-4947-8393-641eefc3ba5e"}
        component = "accounts.CreateAccount"
        self.StaxContract.validate(data, component)
        schema = self.StaxContract.get_schema()
        self.assertEqual(schema.get("info").get("title"), "Stax Core API")

    def testSchemaExceptions(self):
        """
        Test the schema exceptions are raised
        """
        data = "unit"
        component = "accounts.ReadAccounts"
        with self.assertRaises(ValidationException):
            self.StaxContract.validate(data, component)

        component = "unit"
        with self.assertRaises(ValidationException):
            self.StaxContract.validate(data, component)


if __name__ == "__main__":
    unittest.main()
