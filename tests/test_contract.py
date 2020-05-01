"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import unittest

from stax.contract import StaxContract


class StaxContractTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def testDefaultContract(self):
        self.StaxContract = StaxContract
        schema = self.StaxContract.default_swagger_template()
        self.assertEqual(schema.get("info").get("title"), "Stax Core API")
        self.assertIsInstance(schema.get("components").get("schemas"), dict)


if __name__ == "__main__":
    unittest.main()
