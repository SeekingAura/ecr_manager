from mypy_boto3_ecr.type_defs import (
    GetAuthorizationTokenResponseTypeDef,
    ListImagesResponseTypeDef,
    ImageIdentifierTypeDef,
)
from mypy_boto3_sts.type_defs import GetCallerIdentityResponseTypeDef

ECRAuthTokenI = GetAuthorizationTokenResponseTypeDef
ECRCallerIdentityI = GetCallerIdentityResponseTypeDef
ECRListImagesI = ListImagesResponseTypeDef

ECRImagesIdI = list[ImageIdentifierTypeDef]
