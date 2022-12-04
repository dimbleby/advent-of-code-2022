from __future__ import annotations

from attr import frozen

from advent.utils import data_dir


@frozen
class Range:
    low: int
    high: int

    @staticmethod
    def from_str(text: str) -> Range:
        lo, hi = text.split("-")
        return Range(int(lo), int(hi))

    def contains(self, other: Range) -> bool:
        return self.low <= other.low and self.high >= other.high

    def overlaps(self, other: Range) -> bool:
        return self.low <= other.high and self.high >= other.low


def solve() -> None:
    input = data_dir() / "day04.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    pairs = [
        tuple(Range.from_str(text) for text in line.split(","))
        for line in data.splitlines()
    ]

    total = 0
    for p in pairs:
        if p[0].contains(p[1]) or p[1].contains(p[0]):
            total += 1

    print(f"Part one: {total}")

    total = 0
    for p in pairs:
        if p[0].overlaps(p[1]):
            total += 1

    print(f"Part two: {total}")
