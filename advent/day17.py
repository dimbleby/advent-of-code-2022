from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from attrs import define, frozen

from advent.utils import data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator


@frozen
class Cell:
    x: int
    y: int

    def move_right(self, count: int = 1) -> Cell:
        return Cell(self.x + count, self.y)

    def move_left(self, count: int = 1) -> Cell:
        return Cell(self.x - count, self.y)

    def move_down(self, count: int = 1) -> Cell:
        return Cell(self.x, self.y + count)


@frozen
class Shape:
    cells: set[Cell]

    def move_right(self, count: int = 1) -> Shape:
        cells = {cell.move_right(count) for cell in self.cells}
        return Shape(cells)

    def move_left(self, count: int = 1) -> Shape:
        cells = {cell.move_left(count) for cell in self.cells}
        return Shape(cells)

    def move_down(self, count: int = 1) -> Shape:
        cells = {cell.move_down(count) for cell in self.cells}
        return Shape(cells)

    def top(self) -> int:
        return min(cell.y for cell in self.cells)

    def bottom(self) -> int:
        return max(cell.y for cell in self.cells)

    def left(self) -> int:
        return min(cell.x for cell in self.cells)

    def right(self) -> int:
        return max(cell.x for cell in self.cells)

    def trim_below(self, row: int) -> Shape:
        cells = {cell for cell in self.cells if cell.y <= row}
        return Shape(cells)

    def __and__(self, other: Shape) -> Shape:
        intersection = self.cells & other.cells
        return Shape(intersection)

    def __or__(self, other: Shape) -> Shape:
        union = self.cells | other.cells
        return Shape(union)

    def __bool__(self) -> bool:
        return bool(self.cells)


SHAPES = [
    Shape({Cell(2, -4), Cell(3, -4), Cell(4, -4), Cell(5, -4)}),
    Shape({Cell(3, -4), Cell(2, -5), Cell(3, -5), Cell(4, -5), Cell(3, -6)}),
    Shape({Cell(2, -4), Cell(3, -4), Cell(4, -4), Cell(4, -5), Cell(4, -6)}),
    Shape({Cell(2, -4), Cell(2, -5), Cell(2, -6), Cell(2, -7)}),
    Shape({Cell(2, -4), Cell(3, -4), Cell(2, -5), Cell(3, -5)}),
]

FLOOR = Shape({Cell(x, 0) for x in range(7)})


@define
class Grid:
    occupied: Shape = FLOOR
    scrolled: int = 0
    _view: int = 50

    def scroll(self) -> None:
        height = -self.occupied.top()
        self.occupied = self.occupied.move_down(height)
        self.occupied = self.occupied.trim_below(self._view)
        self.scrolled += height

    def drop(self, jets: Iterator[str], shape: Shape) -> int:
        jets_used = 0
        while True:
            jet = next(jets)
            jets_used += 1
            if jet == "<":
                moved = shape.move_left()
                if moved.left() >= 0 and not moved & self.occupied:
                    shape = moved
            else:
                moved = shape.move_right()
                if moved.right() < 7 and not moved & self.occupied:
                    shape = moved

            dropped = shape.move_down()
            if dropped & self.occupied:
                break

            assert dropped.bottom() < self._view
            shape = dropped

        self.occupied |= shape
        self.scroll()

        return jets_used

    def fingerprint(self) -> int:
        return hash(frozenset(self.occupied.cells))


def solve() -> None:
    input = data_dir() / "day17.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read().strip()

    jets = itertools.cycle(data)
    grid = Grid()
    for count, shape in enumerate(itertools.cycle(SHAPES), 1):
        grid.drop(jets, shape)
        if count == 2022:
            break

    print(f"Part one: {grid.scrolled}")

    jets = itertools.cycle(data)
    markers: dict[tuple[int, int, int], tuple[int, int]] = {}
    heights: dict[int, int] = {}
    shape_index = jet_index = 0
    grid = Grid()
    for count, shape in enumerate(itertools.cycle(SHAPES), 1):
        jets_used = grid.drop(jets, shape)
        jet_index += jets_used
        jet_index %= len(data)

        shape_index += 1
        shape_index %= len(SHAPES)

        heights[count] = grid.scrolled

        fingerprint = grid.fingerprint()
        marker = (fingerprint, jet_index, shape_index)
        previously, height = markers.setdefault(marker, (count, grid.scrolled))
        if previously != count:
            cycle_length = count - previously
            cycle_height = grid.scrolled - height

            cycles = 1000000000000 // cycle_length
            base = 1000000000000 % cycle_length
            while base < previously:
                base += cycle_length
                cycles -= 1

            print(f"Part two: {heights[base] + cycles * cycle_height}")
            break
