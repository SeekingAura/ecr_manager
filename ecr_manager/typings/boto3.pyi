from mypy_boto3_ecr import ECRClient as StubECRClient
from mypy_boto3_ecr.type_defs import (
    GetAuthorizationTokenResponseTypeDef,
    ImageIdentifierTypeDef,
    ListImagesResponseTypeDef,
)
from mypy_boto3_sts import STSClient as StubSTSClient
from mypy_boto3_sts.type_defs import GetCallerIdentityResponseTypeDef

# Clients
STSClientI = StubSTSClient

ECRClientI = StubECRClient

ECRAuthTokenI = GetAuthorizationTokenResponseTypeDef

ECRCallerIdentityI = GetCallerIdentityResponseTypeDef
ECRListImagesI = ListImagesResponseTypeDef

ECRImagesIdI = list[ImageIdentifierTypeDef]
