import argparse
from typing import TypedDict


class ExampleValue(TypedDict):
    run: str


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
)
args_namespace: argparse.Namespace = parser.parse_args()
