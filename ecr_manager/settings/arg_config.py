import argparse
import os
from pathlib import Path

from typings.argparser_custom import ECRCliArgs

from .settings import DATA_DIR

# Parser config
parser: argparse.ArgumentParser = argparse.ArgumentParser(
    description="ECR Manager",
)
parser.add_argument(
    "-rn",
    "--run",
    type=str,
    choices=(
        "cli",
        "gui",
    ),
    default="cli",
    help="Determines run mode, default cli",
)
parser.add_argument(
    "-datai",
    "--data-input",
    type=os.path.abspath,
    default=os.path.abspath(Path(DATA_DIR, "images_data.json")),
    help=(
        "load run json file with info of docker images Default "
        f"{os.path.abspath(Path(DATA_DIR, 'images_data.json'))}"
    ),
)

args_namespace: ECRCliArgs = ECRCliArgs(**vars(parser.parse_args()))
