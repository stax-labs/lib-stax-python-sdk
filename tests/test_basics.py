"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import os
import sys
import unittest
import json
import uuid
import boto3

from stax.config import Config

class StaxTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def setUp(self):
        pass

    def testPing(self):
        """
        Test a simple route
        """
        pass


if __name__ == "__main__":
    unittest.main()
