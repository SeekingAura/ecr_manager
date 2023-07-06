from mypy_boto3_ecr import ECRClient as StubECRClient
from mypy_boto3_ecr.type_defs import (
    GetAuthorizationTokenResponseTypeDef,
    ImageIdentifierTypeDef,
    ListImagesResponseTypeDef,
)
from mypy_boto3_sts.type_defs import GetCallerIdentityResponseTypeDef

ECRClientI = StubECRClient
ECRAuthTokenI = GetAuthorizationTokenResponseTypeDef
ECRCallerIdentityI = GetCallerIdentityResponseTypeDef

ECRListImagesI = ListImagesResponseTypeDef
ECRImageIdI = ImageIdentifierTypeDef
