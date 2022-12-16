from __future__ import annotations

import itertools
import re
from typing import ClassVar, Sequence

from attrs import frozen

from advent.utils import data_dir


@frozen
class Valve:
    REGEX: ClassVar[re.Pattern[str]] = re.compile(
        r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    )

    name: str
    flow: int
    neighbours: list[str]

    @staticmethod
    def from_line(line: str) -> Valve:
        m = re.match(Valve.REGEX, line)
        assert m is not None
        name = m.group(1)
        flow = int(m.group(2))
        neighbours = m.group(3).split(", ")
        return Valve(name, flow, neighbours)


@frozen
class Cursor:
    location: str = "AA"
    done: int = 0


@frozen
class State:
    cursors: list[Cursor]
    open: int = 0
    flow: int = 0
    released: int = 0
    time: int = 0


@frozen
class Puzzle:
    valves: dict[str, Valve]
    # sorted best to worst
    useful: list[Valve]
    distances: dict[tuple[str, str], int]
    min_useful_distance: int
    bits: dict[str, int]

    @staticmethod
    def from_valves(valves: list[Valve]) -> Puzzle:
        lookup = {valve.name: valve for valve in valves}

        useful = [valve for valve in valves if valve.flow > 0]
        useful.sort(key=lambda v: v.flow, reverse=True)

        distances = Puzzle.get_distance_table(valves)

        min_useful_distance = min(
            distances[(v1.name, v2.name)]
            for v1 in useful
            for v2 in useful
            if v1.name != v2.name
        )

        bits = {valve.name: 1 << index for index, valve in enumerate(useful)}

        return Puzzle(lookup, useful, distances, min_useful_distance, bits)

    @staticmethod
    def get_distance_table(valves: list[Valve]) -> dict[tuple[str, str], int]:
        # Floyd-Warshall.
        distances = {(v1.name, v2.name): 1000 for v1 in valves for v2 in valves}
        for v1 in valves:
            distances[(v1.name, v1.name)] = 0
            for v2 in v1.neighbours:
                distances[(v1.name, v2)] = 1

        for vk in valves:
            for vi in valves:
                for vj in valves:
                    i, j, k = [valve.name for valve in (vi, vj, vk)]
                    distance_via_k = distances[(i, k)] + distances[(k, j)]
                    if distances[(i, j)] > distance_via_k:
                        distances[(i, j)] = distance_via_k

        return distances

    def bound(self, max_time: int, state: State) -> int:
        now = state.time
        flow = state.flow
        released = state.released

        # Can't do better than going most to least valuable.
        unopened = [
            valve for valve in self.useful if not state.open & self.bits[valve.name]
        ]

        # Calculate the most optimistic schedule for openings.
        schedules: list[Sequence[int]] = []
        for cursor in state.cursors:
            start = cursor.done
            if start == now:
                start += self.min_useful_distance + 1
            schedule = range(start, max_time, self.min_useful_distance + 1)
            schedules.append(schedule)

        openings = sorted(itertools.chain(*schedules))
        for valve, moment in zip(unopened, openings):
            released += flow * (moment - now)
            flow += valve.flow
            now = moment

        return released + (max_time - now) * flow

    def projection(self, max_time: int, state: State) -> int:
        return state.released + (max_time - state.time) * state.flow

    def neighbours(self, max_time: int, state: State) -> list[State]:
        neighbours: list[State] = []

        # Construct the possible useful moves for each cursor.
        unopened = [
            valve for valve in self.useful if not state.open & self.bits[valve.name]
        ]
        all_moves: list[list[Cursor]] = [[] for _ in state.cursors]
        for cursor, moves in zip(state.cursors, all_moves):
            # Consider staying still...
            done = cursor.done if state.time < cursor.done else max_time
            moves.append(Cursor(cursor.location, done))

            # ... and consider moving.
            if state.time == cursor.done:
                for valve in unopened:
                    distance = self.distances[(cursor.location, valve.name)]
                    done = state.time + distance + 1
                    if done < max_time:
                        moves.append(Cursor(valve.name, done))

        # Construct the corresponding neighbours in state-space.
        for new_cursors in itertools.product(*all_moves):
            destinations = set(cursor.location for cursor in new_cursors)
            if len(destinations) < len(new_cursors):
                continue

            new_time = min(cursor.done for cursor in new_cursors)
            new_released = state.released + state.flow * (new_time - state.time)
            new_flow = state.flow
            new_open = state.open
            for cursor in new_cursors:
                if new_time == cursor.done:
                    new_open |= self.bits.get(cursor.location, 0)
                    new_flow += self.valves[cursor.location].flow

            neighbour_state = State(
                list(new_cursors), new_open, new_flow, new_released, new_time
            )
            neighbours.append(neighbour_state)

        return neighbours

    def solve(self, max_time: int, num_cursors: int = 1) -> int:
        start = State([Cursor()] * num_cursors)
        best_release = 0
        stack = [start]
        while stack:
            state = stack.pop()
            bound = self.bound(max_time, state)
            if bound <= best_release:
                continue

            projection = self.projection(max_time, state)
            if projection > best_release:
                best_release = projection

            stack += self.neighbours(max_time, state)

        return best_release


def solve() -> None:
    input = data_dir() / "day16.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    valves = [Valve.from_line(line) for line in data.splitlines()]
    puzzle = Puzzle.from_valves(valves)

    best_release = puzzle.solve(30)
    print(f"Part one: {best_release}")

    best_release = puzzle.solve(26, num_cursors=2)
    print(f"Part two: {best_release}")
