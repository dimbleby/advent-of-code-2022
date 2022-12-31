from __future__ import annotations

from collections import deque
from typing import TypeAlias

from attrs import Factory, define, field, frozen

from advent.utils import data_dir

Coord: TypeAlias = tuple[int, int]


@frozen
class State:
    place: Coord
    time: int


@define
class Map:
    rights: set[Coord]
    lefts: set[Coord]
    downs: set[Coord]
    ups: set[Coord]
    rows: int
    cols: int
    occupied_cache: dict[int, set[Coord]] = field(default=Factory(dict))

    @staticmethod
    def from_text(text: str) -> Map:
        rights: set[Coord] = set()
        lefts: set[Coord] = set()
        downs: set[Coord] = set()
        ups: set[Coord] = set()
        lines = text.splitlines()
        for row, line in enumerate(lines[1:-1]):
            for column, char in enumerate(line[1:-1]):
                match char:
                    case ">":
                        rights.add((row, column))

                    case "<":
                        lefts.add((row, column))

                    case "^":
                        ups.add((row, column))

                    case "v":
                        downs.add((row, column))

        rows = row + 1
        cols = column + 1

        return Map(rights, lefts, downs, ups, rows, cols)

    def occupied_at(self, time: int) -> set[Coord]:
        cached = self.occupied_cache.get(time)
        if cached is not None:
            return cached

        lefts = {(row, (col - time) % self.cols) for row, col in self.lefts}
        rights = {(row, (col + time) % self.cols) for row, col in self.rights}
        ups = {((row - time) % self.rows, col) for row, col in self.ups}
        downs = {((row + time) % self.rows, col) for row, col in self.downs}

        occupied = lefts | rights | ups | downs
        self.occupied_cache[time] = occupied

        return occupied

    def neighbours(self, state: State) -> list[State]:
        neighbours: list[State] = []

        new_time = state.time + 1
        occupied = self.occupied_at(new_time)

        row, col = state.place
        for drow, dcol in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
            new_row = row + drow
            new_col = col + dcol

            if not 0 <= new_row < self.rows:
                if (new_row, new_col) not in {(-1, 0), (self.rows, self.cols - 1)}:
                    continue

            if not 0 <= new_col < self.cols:
                continue

            if (new_row, new_col) in occupied:
                continue

            new_place = (new_row, new_col)
            neighbour = State(new_place, new_time)
            neighbours.append(neighbour)

        return neighbours

    def earliest_arrival(self, end: Coord, start: State) -> int:
        seen: set[State] = set()
        queue = deque([start])
        while queue:
            state = queue.popleft()

            if state.place == end:
                return state.time

            if state in seen:
                continue

            seen.add(state)

            queue += self.neighbours(state)

        raise AssertionError("No path found")


def solve() -> None:
    input = data_dir() / "day24.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    puzzle = Map.from_text(data)
    start = (-1, 0)
    end = (puzzle.rows, puzzle.cols - 1)
    state = State(start, 0)
    arrival = puzzle.earliest_arrival(end, state)

    print(f"Part one: {arrival}")

    state = State(end, arrival)
    arrival = puzzle.earliest_arrival(start, state)

    state = State(start, arrival)
    arrival = puzzle.earliest_arrival(end, state)

    print(f"Part two: {arrival}")
