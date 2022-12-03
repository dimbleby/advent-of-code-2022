from pathlib import Path
from typing import Iterator, TypeVar

T = TypeVar("T")


def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def chunks(lst: list[T], n: int) -> Iterator[list[T]]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
