import unittest

from botocore.stub import Stubber
from unittest.mock import patch

from staxapp.aws_srp import AWSSRP, ForceChangePasswordException


def _mock_authenticate_user(_, client=None):
    return {
        'AuthenticationResult': {
            'TokenType': 'admin',
            'IdToken': 'dummy_token',
            'AccessToken': 'dummy_token',
            'RefreshToken': 'dummy_token'
        }
    }


def _mock_get_params(_):
    return {'USERNAME': 'bob', 'SRP_A': 'srp'}

class AWSSRPTestCase(unittest.TestCase):

    def setUp(self):
        self.app_id = "test"
        self.aws = AWSSRP(username="test",
                          password="test",
                          pool_region='us-east-1',
                          pool_id="test",
                          client_id="test",
                          client_secret="test")

    def tearDown(self):
        del self.aws

    def test_pool_region_validation(self):
        with self.assertRaises(ValueError):
            AWSSRP(username="test",
                   password="test",
                   pool_region='us-east-1',
                   pool_id="test",
                   client_id="test",
                   client_secret="test", client="test")

    def test_calculate_a_safety_check(self):
        self.aws = AWSSRP(username="test",
               password="test",
               pool_region='us-east-1',
               pool_id="test",
               client_id="test",
               client_secret="test")
        self.aws.big_n = 1
        self.aws.small_a_value = 1
        with self.assertRaises(ValueError):
            self.aws.calculate_a()

    def test_calculate_auth_request_check(self):
        self.aws = AWSSRP(username="test",
               password="test",
               pool_region='us-east-1',
               pool_id="test",
               client_id="test",
               client_secret="test")
        self.aws.get_auth_params()

    def test_get_password_authentication_key(self):
        self.aws = AWSSRP(username="test",
               password="test",
               pool_region='us-east-1',
               pool_id="test_test",
               client_id="test",
               client_secret="test")
        self.large_a_value = 0
        self.aws.get_password_authentication_key("test", "test", 0, 1234567890)

    def test_process_challenge_check(self):
        self.aws = AWSSRP(username="test",
               password="test",
               pool_region='us-east-1',
               pool_id="test_test",
               client_id="test",
               client_secret="test")
        resp = self.aws.process_challenge({'USER_ID_FOR_SRP': 'test', 'SALT': '16', 'SRP_B': '16', 'SECRET_BLOCK': 'c2VjcmV0c3NlY3Jlc3Rzc2VjcmV0cwo='})
        self.assertTrue('PASSWORD_CLAIM_SIGNATURE' in resp)

    def test_get_secret_hash(self):
        result = AWSSRP.get_secret_hash("test", "test", "test")
        self.assertIsNotNone(result)

    @patch('staxapp.aws_srp.AWSSRP.get_auth_params', _mock_get_params)
    @patch('staxapp.aws_srp.AWSSRP.process_challenge', return_value={})
    def test_authenticate_user_password_change_challenge(self, _):

        stub = Stubber(self.aws.client)

        # By the stubber nature, we need to add the sequence
        # of calls for the AWS SRP auth to test the whole process
        stub.add_response(method='initiate_auth',
                          service_response={
                              'ChallengeName': 'PASSWORD_VERIFIER',
                              'ChallengeParameters': {}
                          },
                          expected_params={
                              'AuthFlow': 'USER_SRP_AUTH',
                              'AuthParameters': _mock_get_params(None),
                              'ClientId': self.app_id
                          })
        stub.add_response(method='respond_to_auth_challenge',
                          service_response={
                              'ChallengeName': 'NEW_PASSWORD_REQUIRED',
                              'AuthenticationResult': {}
                          },
                          expected_params={
                              'ClientId': self.app_id,
                              'ChallengeName': 'PASSWORD_VERIFIER',
                              'ChallengeResponses': {}
                          })
        with stub:
            with self.assertRaises(ForceChangePasswordException):
                self.aws.authenticate_user()

    @patch('staxapp.aws_srp.AWSSRP.get_auth_params', _mock_get_params)
    @patch('staxapp.aws_srp.AWSSRP.process_challenge', return_value={})
    def test_authenticate_user_bad_challenge(self, _):

        stub = Stubber(self.aws.client)

        # By the stubber nature, we need to add the sequence
        # of calls for the AWS SRP auth to test the whole process
        stub.add_response(method='initiate_auth',
                          service_response={
                              'ChallengeName': 'BOO',
                              'ChallengeParameters': {}
                          },
                          expected_params={
                              'AuthFlow': 'USER_SRP_AUTH',
                              'AuthParameters': _mock_get_params(None),
                              'ClientId': self.app_id
                          })
        with stub:
            with self.assertRaises(NotImplementedError):
                self.aws.authenticate_user()

    @patch('staxapp.aws_srp.AWSSRP.get_auth_params', _mock_get_params)
    @patch('staxapp.aws_srp.AWSSRP.process_challenge', return_value={})
    def test_authenticate_user(self, _):

        stub = Stubber(self.aws.client)

        # By the stubber nature, we need to add the sequence
        # of calls for the AWS SRP auth to test the whole process
        stub.add_response(method='initiate_auth',
                          service_response={
                              'ChallengeName': 'PASSWORD_VERIFIER',
                              'ChallengeParameters': {}
                          },
                          expected_params={
                              'AuthFlow': 'USER_SRP_AUTH',
                              'AuthParameters': _mock_get_params(None),
                              'ClientId': self.app_id
                          })

        stub.add_response(method='respond_to_auth_challenge',
                          service_response={
                              'AuthenticationResult': {
                                  'IdToken': 'dummy_token',
                                  'AccessToken': 'dummy_token',
                                  'RefreshToken': 'dummy_token'
                              }
                          },
                          expected_params={
                              'ClientId': self.app_id,
                              'ChallengeName': 'PASSWORD_VERIFIER',
                              'ChallengeResponses': {}
                          })

        with stub:
            tokens = self.aws.authenticate_user()
            self.assertTrue('IdToken' in tokens['AuthenticationResult'])
            self.assertTrue('AccessToken' in tokens['AuthenticationResult'])
            self.assertTrue('RefreshToken' in tokens['AuthenticationResult'])
            stub.assert_no_pending_responses()


if __name__ == '__main__':
    unittest.main()