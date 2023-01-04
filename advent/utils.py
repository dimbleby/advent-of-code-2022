from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterator

T = TypeVar("T")


def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def chunks(lst: list[T], n: int) -> Iterator[list[T]]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
