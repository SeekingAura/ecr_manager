"""
Load vars for project
"""

from pathlib import Path

from dotenv import (
    find_dotenv,
    load_dotenv,
)


def load_env_vars() -> None:
    from .settings import BASE_DIR

    load_dotenv(
        dotenv_path=find_dotenv(
            filename=Path(BASE_DIR, ".env").__str__(),
        ),
    )
