from pathlib import Path


def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"
