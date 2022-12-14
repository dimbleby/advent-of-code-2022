from copy import deepcopy

from attrs import define, frozen

from advent.utils import data_dir


@frozen
class Cell:
    x: int
    y: int


@define
class Map:
    occupied: set[Cell] = set()
    maxy: int = 0

    def add_rock_path(self, text: str) -> None:
        cells: list[Cell] = []
        for word in text.split(" "):
            if word == "->":
                continue

            x, y = word.split(",")
            cell = Cell(int(x), int(y))
            cells.append(cell)

        for c1, c2 in zip(cells, cells[1:]):
            self.add_rock_line(c1, c2)

    def add_rock_line(self, c1: Cell, c2: Cell) -> None:
        x1, x2 = (c1.x, c2.x) if c1.x <= c2.x else (c2.x, c1.x)
        y1, y2 = (c1.y, c2.y) if c1.y <= c2.y else (c2.y, c1.y)
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.occupied.add(Cell(x, y))
                self.maxy = max(self.maxy, y)

    def add_sand(self, start: Cell, floor: bool = False) -> bool:
        if start in self.occupied:
            return False

        x, y = start.x, start.y
        while True:
            if not floor and y == self.maxy:
                return False

            if y == self.maxy + 1:
                self.occupied.add(Cell(x, y))
                return True

            for dx in (0, -1, 1):
                candidate = Cell(x + dx, y + 1)
                if candidate not in self.occupied:
                    x = x + dx
                    y = y + 1
                    break

            else:
                self.occupied.add(Cell(x, y))
                return True


def solve() -> None:
    input = data_dir() / "day14.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    slice = Map()
    for line in data.splitlines():
        slice.add_rock_path(line)

    count = 0
    start = Cell(500, 0)
    part1 = deepcopy(slice)
    while part1.add_sand(start):
        count += 1

    print(f"Part one: {count}")

    count = 0
    while slice.add_sand(start, floor=True):
        count += 1

    print(f"Part two: {count}")
