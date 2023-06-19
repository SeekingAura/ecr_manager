from pathlib import (
    Path,
    PosixPath,
)

from dotenv import (
    find_dotenv,
    load_dotenv,
)


BASE_DIR: PosixPath = Path(__file__).resolve().parent
load_dotenv(
    dotenv_path=find_dotenv(
        filename=Path(BASE_DIR, ".env"),
    ),
)
