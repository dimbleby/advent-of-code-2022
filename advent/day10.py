from __future__ import annotations

from abc import ABC, abstractmethod

from attrs import define, frozen

from advent.utils import data_dir


class Instruction(ABC):
    @staticmethod
    def from_text(line: str) -> Instruction:
        words = line.split(" ")
        if words[0] == "noop":
            return NoOp()

        if words[0] == "addx":
            return Addx(int(words[1]))

        assert False

    @property
    @abstractmethod
    def cycles(self) -> int:
        ...

    @abstractmethod
    def apply(self, cpu: CPU) -> None:
        ...


@frozen
class NoOp(Instruction):
    @property
    def cycles(self) -> int:
        return 1

    def apply(self, cpu: CPU) -> None:
        pass


@frozen
class Addx(Instruction):
    value: int

    @property
    def cycles(self) -> int:
        return 2

    def apply(self, cpu: CPU) -> None:
        cpu.x += self.value


@define
class CPU:
    program: list[Instruction]
    x: int = 1
    active: Instruction | None = None
    active_age: int = 0

    def tick(self) -> None:
        if self.active is not None:
            self.active_age += 1

            if self.active_age == self.active.cycles:
                self.active.apply(self)
                self.active = None
                self.active_age = 0

        if self.active is None:
            self.active = self.program.pop(0)


def solve() -> None:
    input = data_dir() / "day10.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    instructions = [Instruction.from_text(line) for line in data.splitlines()]

    cpu = CPU(program=instructions[:])
    total = 0
    for cycle in range(1, 221):
        cpu.tick()
        if (cycle % 40) == 20:
            total += cycle * cpu.x

    print(f"Part one: {total}")

    cpu = CPU(program=instructions[:])
    screen = [[" "] * 40 for _ in range(6)]
    for row in range(6):
        for column in range(40):
            cpu.tick()
            if cpu.x - 1 <= column <= cpu.x + 1:
                screen[row][column] = "#"

    print("Part two:")
    for line in screen:
        print("".join(line))
