from typing import Any
from unittest.mock import Mock

import boto3
import docker
import settings as settings

settings.AWS_DEFAULT_REGION = "us-east-1"
settings.AWS_ACCESS_KEY_ID = "test_key_id"
settings.AWS_SECRET_ACCESS_KEY = "test_secret_key"


def boto3_clients(
    service_name: str,
    # region_name=aws_region_name or self.aws_default_region,
    # aws_access_key_id=self.aws_access_key_id,
    # aws_secret_access_key=self.aws_secret_access_key,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any],
) -> dict[str, str] | dict[str, list[dict[str, str]]] | None:
    if service_name == "sts":
        return {
            "Account": "123456789012",
            "UserId": "test_user",
            "Arn": "arn:aws:iam::123456789012:user/test_user",
        }

    if service_name == "ecr":
        return {
            "authorizationData": [
                {
                    "authorizationToken": "dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ=",
                    "proxyEndpoint": (
                        "https://test.dkr.ecr.us-east-1.amazonaws.com"
                    ),
                }
            ]
        }


boto3.client = Mock(side_effect=boto3_clients)

docker.from_env = Mock()
