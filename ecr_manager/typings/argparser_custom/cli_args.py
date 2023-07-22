import argparse
from dataclasses import dataclass


@dataclass
class ECRCliArgs(argparse.Namespace):
    run: str
    data_input: str
