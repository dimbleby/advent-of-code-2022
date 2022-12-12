from __future__ import annotations

from typing import Iterable

from attrs import frozen

from advent.utils import data_dir


@frozen
class Cell:
    x: int
    y: int


@frozen
class HeightMap:
    heights: dict[Cell, int]
    start: Cell
    end: Cell

    def neighbours(self, cell: Cell) -> Iterable[Cell]:
        height = self.heights[cell]
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in moves:
            neighbour = Cell(cell.x + dx, cell.y + dy)
            neighbour_height = self.heights.get(neighbour)
            if neighbour_height is not None and neighbour_height <= height + 1:
                yield neighbour

    def get_route_length(self, part_one: bool = True) -> int:
        visited = (
            {self.start}
            if part_one
            else {cell for cell, height in self.heights.items() if height == 0}
        )
        queue = [(cell, 0) for cell in visited]
        while queue:
            cell, distance = queue.pop(0)
            if cell == self.end:
                return distance

            for neighbour in self.neighbours(cell):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, distance + 1))

        raise AssertionError


def solve() -> None:
    input = data_dir() / "day12.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    heights: dict[Cell, int] = {}
    start = None
    end = None
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            cell = Cell(x, y)
            if char == "S":
                start = cell
                height = 0
            elif char == "E":
                end = cell
                height = 25
            else:
                height = ord(char) - ord("a")

            heights[cell] = height

    assert start is not None
    assert end is not None
    map = HeightMap(heights, start, end)

    print(f"Part one: {map.get_route_length()}")
    print(f"Part two: {map.get_route_length(part_one=False)}")
