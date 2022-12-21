from __future__ import annotations

import operator
from collections import deque
from typing import Callable

from attrs import frozen

from advent.utils import data_dir

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


@frozen
class Expression:
    left: str
    op: Callable[[int, int], int]
    right: str


@frozen
class Monkey:
    name: str
    literal: int | None = None
    expression: Expression | None = None

    @staticmethod
    def from_line(line: str) -> Monkey:
        name = line[:4]
        words = line[6:].split(" ")
        if len(words) == 1:
            literal = int(words[0])
            return Monkey(name, literal=literal)

        expression = Expression(words[0], OPS[words[1]], words[2])
        return Monkey(name, expression=expression)

    def evaluate(self, evaluations: dict[str, int]) -> int:
        if self.literal is not None:
            return self.literal

        assert self.expression is not None
        left = evaluations[self.expression.left]
        right = evaluations[self.expression.right]
        return self.expression.op(left, right)


def topological_sort(monkeys: dict[str, Monkey]) -> list[str]:
    order: list[str] = []

    in_degrees: dict[str, int] = {name: 0 for name in monkeys}
    for monkey in monkeys.values():
        if monkey.expression is not None:
            in_degrees[monkey.expression.left] += 1
            in_degrees[monkey.expression.right] += 1

    queue: deque[str] = deque(
        name for name, in_degree in in_degrees.items() if in_degree == 0
    )
    while queue:
        name = queue.popleft()
        order.append(name)
        monkey = monkeys[name]
        if monkey.expression is not None:
            for neighbour in (monkey.expression.left, monkey.expression.right):
                in_degrees[neighbour] -= 1
                if in_degrees[neighbour] == 0:
                    queue.append(neighbour)

    order.reverse()
    return order


def solve() -> None:
    input = data_dir() / "day21.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    monkeys: dict[str, Monkey] = {}
    for line in data.splitlines():
        monkey = Monkey.from_line(line)
        monkeys[monkey.name] = monkey

    order = topological_sort(monkeys)
    evaluations: dict[str, int] = {}
    for name in order:
        monkey = monkeys[name]
        evaluations[name] = monkey.evaluate(evaluations)

    print(f"Part one: {evaluations['root']}")

    root = monkeys["root"]
    assert root.expression is not None
    left = root.expression.left
    right = root.expression.right

    # Observations: right monkey does not depend on human, left monkey decreases.
    answer: int | None = None
    target = evaluations[right]
    lo = 0
    hi = 100000000000000
    while lo <= hi:
        mid = (lo + hi) // 2
        monkeys["humn"] = Monkey("humn", literal=mid)
        for name in order:
            monkey = monkeys[name]
            evaluations[name] = monkey.evaluate(evaluations)
        value = evaluations[left]

        if value < target:
            hi = mid + 1
        elif value > target:
            lo = mid - 1
        else:
            answer = mid
            break

    assert answer is not None
    print(f"Part two: {answer}")
