import base64
import json
import logging
import logging.config
from pathlib import Path
from typing import TYPE_CHECKING

import boto3
import docker
from settings import DATA_DIR

if TYPE_CHECKING:
    from typings.boto3 import (
        IECRClient,
        IECRImageId,
        IECRListImages,
        ISTSClient,
        IECRAuthToken,
        IECRCallerIdentity,
        IECRBatchDeleteImageResponse,
    )
    from .typings.docker import DockerClient as IDockerClient
    from .typings.ecr_manager import IDockerImagesData

import settings.settings as settings


def main() -> None:
    # Load settings vars
    AWS_ACCESS_KEY_ID: str = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY: str = settings.AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION: str = settings.AWS_DEFAULT_REGION

    aws_ecr: IECRClient = boto3.client(
        service_name="ecr",
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    aws_sts: ISTSClient = boto3.client(
        service_name="sts",
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    ecr_auth: IECRAuthToken = aws_ecr.get_authorization_token()

    caller_identity: IECRCallerIdentity = aws_sts.get_caller_identity()

    docker_client: IDockerClient = docker.from_env()

    username: str = "AWS"
    password: str = ecr_auth.get("authorizationData")[0].get(
        "authorizationToken",
        "",
    )

    username, password = (
        base64.b64decode(password)
        .decode("utf-8")
        .split(
            ":",
            maxsplit=1,
        )
    )

    aws_account_id: str = caller_identity.get("Account")

    registry: str = (
        f"{aws_account_id}.dkr.ecr.{AWS_DEFAULT_REGION}.amazonaws.com"
    )

    docker_client.login(
        username=username,
        password=password,
        registry=registry,
    )

    # Images to push
    with open(Path(DATA_DIR, "images_data.json"), "r") as file_read:
        images_data: IDockerImagesData = json.load(file_read)

    # Get untagged/dangling images BEFORE to push
    images_untag_before: dict[
        str,
        list[IECRImageId],
    ] = dict()

    for image_name_i in images_data.get("images").keys():
        images_list_i: IECRListImages = aws_ecr.list_images(
            repositoryName=image_name_i,
            filter={
                "tagStatus": "UNTAGGED",
            },
        )
        images_untag_before[image_name_i] = images_list_i.get("imageIds")

    uploaded_images_status: dict[str, str] = dict()
    # Push images
    for image_name_i, image_tag_i in images_data.get("images").items():
        repository_i: str = f"{registry}/{image_name_i}"
        logging.info(f"pushing {repository_i}")
        pushed = False
        for push_info in docker_client.images.push(
            repository=repository_i,
            tag=image_tag_i,
            stream=True,
            decode=True,
        ):
            logging.info(push_info)
            if not pushed and push_info.get("status") == "Pushing":
                uploaded_images_status[image_name_i] = "Pushed"
                pushed = True

    # Everything is ok delete old dangling images
    for image_name_i, images_i in images_untag_before.items():
        upload_status: str = uploaded_images_status.get(image_name_i, "")
        if not upload_status:
            logging.warning(
                f'Image "{image_name_i}" not uploaded, UNTAGGED images skip '
                "delete"
            )
            continue
        if images_i:
            response_delete: IECRBatchDeleteImageResponse = (
                aws_ecr.batch_delete_image(
                    repositoryName=image_name_i,
                    imageIds=images_i,
                )
            )
            logging.info(response_delete)
        else:
            logging.warning(
                (
                    f"repo: {image_name_i}, does not have UNTAGGED images to "
                    "delete"
                ),
            )

    logging.debug("Remember AWS cli vars")
    logging.debug(f'export AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID}"')
    logging.debug(f'export AWS_SECRET_ACCESS_KEY=f"{AWS_SECRET_ACCESS_KEY}"')
    logging.debug(f'export AWS_DEFAULT_REGION="{AWS_DEFAULT_REGION}"')
    logging.debug(f'export AWS_ACCOUNT_ID="{aws_account_id}"')

    logging.debug("Remember login command")
    logging.debug(
        (
            f"aws ecr get-login-password --region {AWS_DEFAULT_REGION} | "
            f"docker login --username AWS --password-stdin {registry}"
        ),
    )
