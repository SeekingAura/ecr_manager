from .boto3 import (
    Session,
    client,
    setup_default_session,
)
from .ecr import (
    ECRAuthTokenI,
    ECRCallerIdentityI,
    ECRClientI,
    ECRImageIdI,
    ECRListImagesI,
)
from .sts import STSClientI

__all__: tuple[str, ...] = (
    "client",
    "ECRAuthTokenI",
    "ECRCallerIdentityI",
    "ECRClientI",
    "ECRImageIdI",
    "ECRListImagesI",
    "Session",
    "setup_default_session",
    "STSClientI",
)
