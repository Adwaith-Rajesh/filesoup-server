from pathlib import Path


def check_file_exists(full_path: str) -> bool:
    return True if Path(full_path).is_file() else False
