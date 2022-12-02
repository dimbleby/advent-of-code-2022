from __future__ import annotations

import itertools

from attrs import frozen

from advent.utils import data_dir


@frozen
class Elf:
    items: list[int]

    def total(self) -> int:
        return sum(self.items)


def solve() -> None:
    input = data_dir() / "day01.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    elves: list[Elf] = []
    for blank, lines in itertools.groupby(data.splitlines(), lambda line: line == ""):
        if blank:
            continue

        items = [int(line) for line in lines]
        elf = Elf(items)
        elves.append(elf)

    part_one = max(elf.total() for elf in elves)
    print(f"Part one: {part_one}")

    totals = sorted((elf.total() for elf in elves), reverse=True)
    part_two = sum(totals[:3])
    print(f"Part two: {part_two}")


if __name__ == "__main__":
    solve()
