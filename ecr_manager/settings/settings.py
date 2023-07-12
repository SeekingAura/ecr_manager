import os
from pathlib import Path

from .var_load import load_env_vars

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

load_env_vars()

AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION: str = os.getenv("AWS_DEFAULT_REGION", "")

DATA_DIR: str = Path(BASE_DIR, os.getenv("DATA_DIR", "data_input/")).__str__()
