import base64
import json
import logging
import logging.config

import boto3
import docker

import settings

from _typing import ImagesData

logging.config.dictConfig(settings.LOGGING)

AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION = settings.AWS_DEFAULT_REGION

aws_ecr = boto3.client(
    service_name="ecr",
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

aws_sts = boto3.client(
    service_name="sts",
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

ecr_auth = aws_ecr.get_authorization_token()

caller_identity = aws_sts.get_caller_identity()

docker_client = docker.from_env()

username = "AWS"
password = ecr_auth.get("authorizationData")[0].get("authorizationToken")

username, password = (
    base64.b64decode(password)
    .decode("utf-8")
    .split(
        ":",
        maxsplit=1,
    )
)

aws_account_id = caller_identity.get("Account")
registry = f"{aws_account_id}.dkr.ecr.{AWS_DEFAULT_REGION}.amazonaws.com"

data = docker_client.login(
    username=username,
    password=password,
    registry=registry,
)

# Images to push
with open("images_data.json", "r") as file_read:
    images_data: ImagesData = json.load(file_read)

# Get untagged images BEFORE to push
images_untag_before = dict()

for image_name_i in images_data.get("images").keys():
    images_list_i = aws_ecr.list_images(
        repositoryName=image_name_i,
        filter={
            "tagStatus": "UNTAGGED",
        },
    )
    images_untag_before[image_name_i] = images_list_i.get("imageIds")


uploaded_images = dict()
# Push images
for image_name_i, image_tag_i in images_data.get("images").items():
    repository_i = f"{registry}/{image_name_i}"
    logging.info(f"pushing {repository_i}")
    pushed = False
    for line in docker_client.images.push(
        repository=repository_i,
        tag=image_tag_i,
        stream=True,
        decode=True,
    ):
        logging.info(line)
        if not pushed and line.get("status") == "Pushing":
            uploaded_images[image_name_i] = "Pushed"
            pushed = True

# Everything is ok delete old images
for image_name_i, images_i in images_untag_before.items():
    upload_status = uploaded_images.get(image_name_i)
    if upload_status is None:
        logging.warning(
            f'Image "{image_name_i}" not uploaded, UNTAGGED images skip delete'
        )
        continue
    if images_i:
        # if (images_data.get(image_name_i)=="latest"):
        response_delete = aws_ecr.batch_delete_image(
            repositoryName=image_name_i,
            imageIds=images_i,
        )
        logging.info(response_delete)
    else:
        logging.warning(
            f"repo: {image_name_i}, do not have UNTAGGED images to delete",
        )

logging.debug("Remember AWS cli vars")
logging.debug(f'export AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID}"')
logging.debug(f'export AWS_SECRET_ACCESS_KEY=f"{AWS_SECRET_ACCESS_KEY}"')
logging.debug(f'export AWS_DEFAULT_REGION="{AWS_DEFAULT_REGION}"')
logging.debug(f'export AWS_ACCOUNT_ID="{aws_account_id}"')

logging.debug("Remember login command")
logging.debug(
    f"aws ecr get-login-password --region {AWS_DEFAULT_REGION} | "
    f"docker login --username AWS --password-stdin {registry}",
)
