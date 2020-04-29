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
        schema = self.StaxContract.default_swagger_template(test_mode=True)
        self.assertEqual(schema.get("info").get("title"), "Stax Core API")


if __name__ == "__main__":
    unittest.main()
