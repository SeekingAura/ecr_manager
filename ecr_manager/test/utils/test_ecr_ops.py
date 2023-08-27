import unittest

from utils.ecr_ops import ECRManager

from .mock_ecr_ops import (
    boto3,
    docker,
)


class TestECRManager(unittest.TestCase):
    """
    A test for the ECRManager
    """

    def setUp(self) -> None:
        """
        Set up the test fixture
        """
        # Create an instance of the ECRManager class
        self.ecr_manager = ECRManager()

        # Mock the ECR client attributes and methods
        self.ecr_manager.aws_ecr.get_authorization_token.return_value = {
            "authorizationData": [
                {
                    "authorizationToken": "dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
                    "proxyEndpoint": (
                        "https://test.dkr.ecr.us-east-1.amazonaws.com"
                    ),
                }
            ]
        }

        # Mock the STS client attributes and methods
        self.ecr_manager.aws_sts.get_caller_identity.return_value = {
            "Account": "123456789012",
            "UserId": "test_user",
            "Arn": "arn:aws:iam::123456789012:user/test_user",
        }

        # Mock the docker client attributes and methods
        self.ecr_manager.docker_client.login.return_value = {
            "Status": "Login Succeeded",
            "IdentityToken": "test_token",
        }

    def test_init(self) -> None:
        """
        Test the __init__ method of the ECRManager
        """
        # Check that the AWS credentials are set correctly
        self.assertEqual(self.ecr_manager.aws_default_region, "us-east-1")
        self.assertEqual(self.ecr_manager.aws_access_key_id, "test_key_id")
        self.assertEqual(
            self.ecr_manager.aws_secret_access_key, "test_secret_key"
        )

        # Check that the ECR client and STS client are created correctly
        boto3.client.assert_any_call(
            service_name="ecr",
            region_name="us-east-1",
            aws_access_key_id="test_key_id",
            aws_secret_access_key="test_secret_key",
        )
        boto3.client.assert_any_call(
            service_name="sts",
            region_name="us-east-1",
            aws_access_key_id="test_key_id",
            aws_secret_access_key="test_secret_key",
        )

        # Check that the AWS account ID and docker registry are set correctly
        self.assertEqual(self.ecr_manager.aws_account_id, "123456789012")
        self.assertEqual(
            self.ecr_manager.docker_registry,
            "123456789012.dkr.ecr.us-east-1.amazonaws.com",
        )

        # Check that the docker client is created correctly
        docker.from_env.assert_called_once()

    def test_get_ecr_docker_credentials(self) -> None:
        """
        Test the get_ecr_docker_credentials method of the ECRManager
        """
        # Call the method and get the username and password
        username, password = self.ecr_manager.get_ecr_docker_credentials()

        # Check that the username and password are correct
        self.assertEqual(username, "test_user")
        self.assertEqual(password, "test_password")

    def test_get_aws_account_id(self) -> None:
        """
        Test the get_aws_account_id method of the ECRManager
        """
        # Call the method and get the AWS account ID
        aws_account_id = self.ecr_manager.get_aws_account_id()

        # Check that the AWS account ID is correct
        self.assertEqual(aws_account_id, "123456789012")

    def test_get_docker_registry(self) -> None:
        """
        Test the get_docker_registry method of the ECRManager
        """
        # Call the method and get the docker registry
        docker_registry = self.ecr_manager.get_docker_registry()

        # Check that the docker registry is correct
        self.assertEqual(
            docker_registry,
            "123456789012.dkr.ecr.us-east-1.amazonaws.com",
        )

    def test_auth_docker(self) -> None:
        """
        Test the auth_docker method of the ECRManager
        """
        # Call the method and authenticate the docker client with ECR
        self.ecr_manager.auth_docker()

        # Check that the docker client login method is called correctly
        self.ecr_manager.docker_client.login.assert_called_once_with(
            username="test_user",
            password="test_password",
            registry="123456789012.dkr.ecr.us-east-1.amazonaws.com",
            reauth=True,
        )
