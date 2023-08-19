from mypy_boto3_ecr import ECRClient as StubECRClient
from mypy_boto3_ecr.type_defs import (
    GetAuthorizationTokenResponseTypeDef,
    ImageIdentifierTypeDef,
    ListImagesResponseTypeDef,
    BatchDeleteImageResponseTypeDef,
)
from mypy_boto3_sts.type_defs import GetCallerIdentityResponseTypeDef

IECRClient = StubECRClient
IECRAuthToken = GetAuthorizationTokenResponseTypeDef
IECRCallerIdentity = GetCallerIdentityResponseTypeDef

IECRListImages = ListImagesResponseTypeDef
IECRImageId = ImageIdentifierTypeDef

IECRBatchDeleteImageResponse = BatchDeleteImageResponseTypeDef
