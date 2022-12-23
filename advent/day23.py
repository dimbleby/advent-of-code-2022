from __future__ import annotations

from collections import defaultdict
from typing import TypeAlias

from attrs import define

from advent.utils import data_dir

Coord: TypeAlias = tuple[int, int]
Direction: TypeAlias = tuple[int, int]

NORTH = (-1, 0)
NORTHEAST = (-1, 1)
EAST = (0, 1)
SOUTHEAST = (1, 1)
SOUTH = (1, 0)
SOUTHWEST = (1, -1)
WEST = (0, -1)
NORTHWEST = (-1, -1)

ADJACENCIES = {
    NORTH: [NORTHWEST, NORTH, NORTHEAST],
    EAST: [NORTHEAST, EAST, SOUTHEAST],
    SOUTH: [SOUTHWEST, SOUTH, SOUTHEAST],
    WEST: [NORTHWEST, WEST, SOUTHWEST],
}


@define
class Map:
    elves: set[Coord]

    @staticmethod
    def from_text(text: str) -> Map:
        elves: set[Coord] = set()
        for row, line in enumerate(text.splitlines()):
            for column, char in enumerate(line):
                if char == "#":
                    elves.add((row, column))

        return Map(elves)

    def has_neighbours(self, elf: Coord, direction: Direction) -> bool:
        row, col = elf
        for drow, dcol in ADJACENCIES[direction]:
            if (row + drow, col + dcol) in self.elves:
                return True

        return False

    def step(self, directions: list[Direction]) -> bool:
        moved = False
        proposals: dict[Coord, list[Coord]] = defaultdict(list)
        for elf in self.elves:
            neighbours = {
                direction: self.has_neighbours(elf, direction)
                for direction in directions
            }
            if not any(neighbours.values()):
                continue

            row, col = elf
            for direction in directions:
                if not neighbours[direction]:
                    drow, dcol = direction
                    proposals[row + drow, col + dcol].append(elf)
                    break

        for proposal, proposers in proposals.items():
            if len(proposers) != 1:
                continue

            self.elves.remove(proposers[0])
            self.elves.add(proposal)
            moved = True

        return moved

    def corners(self) -> tuple[Coord, Coord]:
        south = max(row for row, _ in self.elves)
        north = min(row for row, _ in self.elves)
        east = max(column for _, column in self.elves)
        west = min(column for _, column in self.elves)

        return ((north, west), (south, east))

    def score(self) -> int:
        ((north, west), (south, east)) = self.corners()
        area = (south + 1 - north) * (east + 1 - west)
        score = area - len(self.elves)
        return score


def solve() -> None:
    input = data_dir() / "day23.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    puzzle = Map.from_text(data)
    directions = [NORTH, SOUTH, WEST, EAST]

    for _ in range(10):
        puzzle.step(directions)
        directions = directions[1:] + directions[:1]

    answer = puzzle.score()
    print(f"Part one: {answer}")

    round = 11
    while puzzle.step(directions):
        round += 1
        directions = directions[1:] + directions[:1]

    print(f"Part two: {round}")
