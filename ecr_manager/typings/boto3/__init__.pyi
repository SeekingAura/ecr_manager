from .boto3 import (
    Session,
    client,
    setup_default_session,
)
from .ecr import (
    ECRAuthTokenI,
    ECRClientI,
    ECRCallerIdentityI,
)
from .sts import STSClientI

__all__: tuple[str, ...] = (
    "client",
    "ECRAuthTokenI",
    "ECRCallerIdentityI",
    "ECRClientI",
    "Session",
    "setup_default_session",
    "STSClientI",
)
