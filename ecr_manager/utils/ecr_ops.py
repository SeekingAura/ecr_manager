import base64
import logging
import logging.config

from typing import TYPE_CHECKING

import boto3

import docker

if TYPE_CHECKING:
    from typings.boto3 import (
        IECRClient,
        ISTSClient,
        IECRAuthToken,
        IECRCallerIdentity,
    )
    from typings.docker import DockerClient as IDockerClient

import settings as settings

logger: logging.Logger = logging.getLogger(__name__)


class ECRManager:
    """
    Manage AWS ECR operations
    """

    # AWS vars
    aws_default_region: str
    aws_access_key_id: str
    aws_secret_access_key: str

    aws_account_id: str

    # Docker vars
    docker_registry: str

    # Client objs
    aws_ecr: "IECRClient"
    aws_sts: "ISTSClient"
    docker_client: "IDockerClient"

    def __init__(
        self,
        aws_default_region: str = "",
        aws_access_key_id: str = "",
        aws_secret_access_key: str = "",
    ) -> None:
        # Load settings vars
        if (
            not aws_default_region
            and not aws_access_key_id
            and not aws_secret_access_key
        ):
            logger.debug(
                "AWS credentials are None, using values from settings"
            )
            aws_default_region = settings.AWS_DEFAULT_REGION
            aws_access_key_id = settings.AWS_ACCESS_KEY_ID
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        elif aws_access_key_id or aws_secret_access_key or aws_default_region:
            raise ValueError(
                "aws config partially configured check values:\n"
                f'aws_default_region: "{aws_default_region}"'
                f'aws_access_key_id: "{aws_access_key_id}"\n'
                f'aws_secret_access_key: "{aws_secret_access_key}"\n'
            )

        # AWS Credentials
        self.aws_default_region: str = aws_default_region
        self.aws_access_key_id: str = aws_access_key_id
        self.aws_secret_access_key: str = aws_secret_access_key

        # Initialize ECR
        self.set_ecr_client()
        self.set_sts_client()

        # Attributes
        self.aws_account_id: str = self.get_aws_account_id()
        self.docker_registry: str = self.get_docker_registry()

        # Docker
        self.docker_registry = self.get_docker_registry()
        self.docker_client: IDockerClient = docker.from_env()

        self.auth_docker()

    def set_ecr_client(
        self,
        aws_region_name: str = "",
    ) -> None:
        aws_region_name = aws_region_name or self.aws_default_region

        self.aws_ecr: IECRClient = boto3.client(
            service_name="ecr",
            region_name=aws_region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def set_sts_client(
        self,
        aws_region_name: str = "",
    ) -> None:
        aws_region_name = aws_region_name or self.aws_default_region

        self.aws_sts: ISTSClient = boto3.client(
            service_name="sts",
            region_name=aws_region_name or self.aws_default_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def get_ecr_docker_credentials(self) -> tuple[str, str]:
        ecr_auth: IECRAuthToken = self.aws_ecr.get_authorization_token()
        print(ecr_auth)
        auth_token: str = ecr_auth.get("authorizationData")[0].get(
            "authorizationToken",
            "",
        )

        username: str
        password: str
        username, password = (
            base64.b64decode(auth_token)
            .decode("utf-8")
            .split(
                ":",
                maxsplit=1,
            )
        )
        return username, password

    def get_aws_account_id(self) -> str:
        """
        Get the AWS root account ID where IAM is related
        """
        caller_identity: IECRCallerIdentity = (
            self.aws_sts.get_caller_identity()
        )

        aws_account_id: str = caller_identity.get("Account")
        return aws_account_id

    def get_docker_registry(
        self,
    ) -> str:
        """Get the docker registry."""
        return (
            f"{self.aws_account_id}"
            ".dkr.ecr."
            f"{self.aws_default_region}.amazonaws.com"
        )

    def auth_docker(
        self,
        docker_registry: str = "",
    ) -> None:
        """
        Authenticate on docker
        """
        docker_registry = docker_registry or self.docker_registry

        username: str
        password: str
        username, password = self.get_ecr_docker_credentials()

        self.docker_client.login(
            username=username,
            password=password,
            registry=docker_registry,
        )

    def upload_images(self):
        pass
