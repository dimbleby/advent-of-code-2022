from __future__ import annotations

import itertools
import operator
from copy import deepcopy
from functools import reduce
from typing import TYPE_CHECKING

from attrs import define

from advent.utils import data_dir

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator


@define
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    divisibility_test: int
    if_true: int
    if_false: int
    inspections: int = 0

    @staticmethod
    def from_text(lines: Iterator[str]) -> Monkey:
        # Don't need the monkey's index.
        next(lines)

        words = next(lines).removeprefix("  Starting items: ").split(", ")
        items = [int(word) for word in words]

        words = next(lines).removeprefix("  Operation: new = old ").split(" ")
        op = operator.add if words[0] == "+" else operator.mul
        operand = words[1]
        operation = (
            (lambda old: op(old, old))
            if operand == "old"
            else (lambda old: op(old, int(operand)))
        )

        word = next(lines).removeprefix("  Test: divisible by ")
        divisibility_test = int(word)

        word = next(lines).removeprefix("    If true: throw to monkey ")
        if_true = int(word)

        word = next(lines).removeprefix("    If false: throw to monkey ")
        if_false = int(word)

        return Monkey(items, operation, divisibility_test, if_true, if_false)

    def turn(self, lcm: int | None = None) -> list[tuple[int, int]]:
        results: list[tuple[int, int]] = []

        while self.items:
            item = self.items.pop()
            item = self.operation(item)
            item = item // 3 if lcm is None else item % lcm
            target = (
                self.if_true if (item % self.divisibility_test) == 0 else self.if_false
            )
            results.append((target, item))

            self.inspections += 1

        return results


def solve() -> None:
    input = data_dir() / "day11.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    start: list[Monkey] = []
    for blank, lines in itertools.groupby(data.splitlines(), lambda line: line == ""):
        if blank:
            continue

        monkey = Monkey.from_text(lines)
        start.append(monkey)

    monkeys = deepcopy(start)
    for _round in range(20):
        for monkey in monkeys:
            for target, item in monkey.turn():
                monkeys[target].items.append(item)

    inspections = sorted([monkey.inspections for monkey in monkeys], reverse=True)
    print(f"Part one: {inspections[0] * inspections[1]}")

    monkeys = deepcopy(start)
    lcm = reduce(operator.mul, (m.divisibility_test for m in monkeys))
    for _round in range(10000):
        for monkey in monkeys:
            for target, item in monkey.turn(lcm=lcm):
                monkeys[target].items.append(item)

    inspections = sorted([monkey.inspections for monkey in monkeys], reverse=True)
    print(f"Part two: {inspections[0] * inspections[1]}")
