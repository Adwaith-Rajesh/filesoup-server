from pathlib import Path
from contextlib import suppress
import os


def check_file_exists(full_path: str) -> bool:
    return True if Path(full_path).is_file() else False


def delete_file(file_path: str) -> None:
    with suppress(FileNotFoundError):
        os.remove(file_path)