import re
from typing import TypeAlias

from attrs import Factory, define, field

from advent.utils import data_dir

Coord: TypeAlias = tuple[int, int]
Direction: TypeAlias = tuple[int, int]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


LEFT_TURNS = {
    DOWN: RIGHT,
    RIGHT: UP,
    UP: LEFT,
    LEFT: DOWN,
}


RIGHT_TURNS = {
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
    UP: RIGHT,
}


DIRECTIONS = {RIGHT: 0, DOWN: 1, LEFT: 2, UP: 3}

# My map is arranged as:
#
#     2211
#     2211
#     33
#     33
#   5544
#   5544
#   66
#   66
#
# which gives the following joins
#
# left of face 2 -> left of face 5
# top of face 2 -> left of face 6
# top of face 1 -> bottom of face 6
# right of face 1 -> right of face 4
# bottom of face 1 -> right of face 3
# left of face 3 -> top of face 5
# bottom of face 4 -> right of face 6
#
# Let's just hardcode the answers.
JOINS: dict[tuple[Coord, Direction], tuple[Coord, Direction]] = {}
for index in range(1, 51):
    JOINS[((index, 50), LEFT)] = ((151 - index, 1), RIGHT)
    JOINS[((151 - index, 0), LEFT)] = ((index, 51), RIGHT)

    JOINS[((0, index + 50), UP)] = ((index + 150, 1), RIGHT)
    JOINS[((index + 150, 0), LEFT)] = ((1, index + 50), DOWN)

    JOINS[((0, index + 100), UP)] = ((200, index), UP)
    JOINS[((201, index), DOWN)] = ((1, index + 100), DOWN)

    JOINS[((index, 151), RIGHT)] = ((151 - index, 100), LEFT)
    JOINS[((151 - index, 101), RIGHT)] = ((index, 150), LEFT)

    JOINS[((51, index + 100), DOWN)] = ((index + 50, 100), LEFT)
    JOINS[((index + 50, 101), RIGHT)] = ((50, index + 100), UP)

    JOINS[((index + 50, 50), LEFT)] = ((101, index), DOWN)
    JOINS[((100, index), UP)] = ((index + 50, 51), RIGHT)

    JOINS[((151, index + 50), DOWN)] = ((index + 150, 50), LEFT)
    JOINS[((index + 150, 51), RIGHT)] = ((150, index + 50), UP)


@define
class Puzzle:
    map: dict[Coord, str]
    position: Coord = field(init=False)
    facing: Direction = RIGHT
    _col_max: dict[int, int] = field(default=Factory(dict))
    _col_min: dict[int, int] = field(default=Factory(dict))
    _row_max: dict[int, int] = field(default=Factory(dict))
    _row_min: dict[int, int] = field(default=Factory(dict))

    def __attrs_post_init__(self) -> None:
        for row, column in self.map:
            row_min = self._row_min.get(row)
            if row_min is None or column < row_min:
                self._row_min[row] = column

            row_max = self._row_max.get(row)
            if row_max is None or column > row_max:
                self._row_max[row] = column

            col_min = self._col_min.get(column)
            if col_min is None or row < col_min:
                self._col_min[column] = row

            col_max = self._col_max.get(column)
            if col_max is None or row > col_max:
                self._col_max[column] = row

        self.position = (1, self._row_min[1])

    def reset(self) -> None:
        self.position = (1, self._row_min[1])
        self.facing = RIGHT

    def wrap_part_one(self, position: Coord) -> Coord:
        row, column = position
        if self.facing == DOWN and row > self._col_max[column]:
            row = self._col_min[column]
        if self.facing == UP and row < self._col_min[column]:
            row = self._col_max[column]
        if self.facing == RIGHT and column > self._row_max[row]:
            column = self._row_min[row]
        if self.facing == LEFT and column < self._row_min[row]:
            column = self._row_max[row]

        return (row, column)

    def wrap_part_two(self, position: Coord) -> tuple[Coord, Direction]:
        wrapped = JOINS.get((position, self.facing))
        return wrapped or (position, self.facing)

    def step_forward(self, part_two: bool = False) -> None:
        row, column = self.position
        drow, dcolumn = self.facing
        new_row, new_column = (row + drow, column + dcolumn)

        if part_two:
            new_position, new_facing = self.wrap_part_two((new_row, new_column))
        else:
            new_position = self.wrap_part_one((new_row, new_column))
            new_facing = self.facing

        if self.map[new_position] != ".":
            return

        self.position = new_position
        self.facing = new_facing

    def act(self, instruction: str, part_two: bool = False) -> None:
        match instruction:
            case "R":
                self.facing = RIGHT_TURNS[self.facing]

            case "L":
                self.facing = LEFT_TURNS[self.facing]

            case distance:
                for _ in range(int(distance)):
                    self.step_forward(part_two)

    def get_password(self) -> int:
        row, column = self.position
        password = 1000 * row + 4 * column + DIRECTIONS[self.facing]
        return password


def solve() -> None:
    input = data_dir() / "day22.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    cells: dict[Coord, str] = {}
    indexed_lines = enumerate(data.splitlines(), 1)
    for row, line in indexed_lines:
        if not line:
            break

        for column, char in enumerate(line, 1):
            if char != " ":
                cells[row, column] = char

    puzzle = Puzzle(cells)

    _, path = next(indexed_lines)
    instructions = re.split(r"(\D+)", path)

    for instruction in instructions:
        puzzle.act(instruction)

    answer = puzzle.get_password()
    print(f"Part one: {answer}")

    puzzle.reset()
    for instruction in instructions:
        puzzle.act(instruction, part_two=True)

    answer = puzzle.get_password()
    print(f"Part two: {answer}")
