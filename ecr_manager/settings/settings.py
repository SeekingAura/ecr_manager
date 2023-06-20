import os

from .var_load import load_env_vars

load_env_vars()

AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION: str = os.getenv("AWS_DEFAULT_REGION", "")
