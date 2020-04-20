"""
Unit test suite for libstax.

To run:
nose2 -v basics
"""

import base64
import os
import sys
import unittest
import json
import jwt
import uuid
import boto3
import logging

from stax.auth import StaxAuth


class StaxAuthTests(unittest.TestCase):
    """
    Inherited class to run all unit tests for this module
    """

    def testStaxAuthInit(self):
        sa = StaxAuth("ApiAuth")
        self.assertEqual(sa.aws_region, "ap-southeast-2")


if __name__ == "__main__":
    unittest.main()
