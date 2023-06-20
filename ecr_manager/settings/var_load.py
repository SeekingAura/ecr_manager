"""
Load vars for project
"""

from pathlib import Path

from dotenv import (
    find_dotenv,
    load_dotenv,
)

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


def load_env_vars() -> None:
    load_dotenv(
        dotenv_path=find_dotenv(
            filename=Path(BASE_DIR, ".env").__str__(),
        ),
    )
