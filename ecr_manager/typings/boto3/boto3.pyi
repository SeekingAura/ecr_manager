from typing import (
    Any,
    Literal,
    overload,
)

from boto3.session import Session as Session

from .ecr import ECRClientI
from .sts import STSClientI

def setup_default_session(**kwargs: Any) -> None: ...
@overload
def client(
    service_name: Literal["ecr",],
    region_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    *args: Any,
    **kwargs: Any,
) -> ECRClientI: ...
@overload
def client(
    service_name: Literal["sts",],
    region_name: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    *args: Any,
    **kwargs: Any,
) -> STSClientI: ...
