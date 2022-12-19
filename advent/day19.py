from __future__ import annotations

import re

from attrs import define, evolve, field, frozen

from advent.utils import data_dir


@frozen
class Stuff:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __add__(self, other: Stuff) -> Stuff:
        return Stuff(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode,
        )

    def __sub__(self, other: Stuff) -> Stuff:
        return Stuff(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode,
        )

    def matches(self, other: Stuff) -> bool:
        return (
            self.ore >= other.ore
            and self.clay >= other.clay
            and self.obsidian >= other.obsidian
            and self.geode >= other.geode
        )


@frozen
class State:
    robots: Stuff = Stuff(ore=1)
    stuff: Stuff = Stuff()
    time: int = 0


@define
class Blueprint:
    ore_cost: Stuff
    clay_cost: Stuff
    obsidian_cost: Stuff
    geode_cost: Stuff
    max_costs: Stuff = field(init=False)

    def __attrs_post_init__(self) -> None:
        costs = [self.ore_cost, self.clay_cost, self.obsidian_cost, self.geode_cost]
        max_ore = max(cost.ore for cost in costs)
        max_clay = max(cost.clay for cost in costs)
        max_obsidian = max(cost.obsidian for cost in costs)
        self.max_costs = Stuff(ore=max_ore, clay=max_clay, obsidian=max_obsidian)

    @staticmethod
    def from_line(line: str) -> Blueprint:
        numbers = [int(number) for number in re.findall(r"(\d+)", line)]
        ore_cost = Stuff(ore=numbers[1])
        clay_cost = Stuff(ore=numbers[2])
        obsidian_cost = Stuff(ore=numbers[3], clay=numbers[4])
        geode_cost = Stuff(ore=numbers[5], obsidian=numbers[6])
        return Blueprint(ore_cost, clay_cost, obsidian_cost, geode_cost)

    def nothing(self, state: State) -> State:
        return State(
            time=state.time + 1, stuff=state.stuff + state.robots, robots=state.robots
        )

    def ore(self, max_time: int, state: State) -> State | None:
        while state.time < max_time and not state.stuff.matches(self.ore_cost):
            state = self.nothing(state)

        if state.time == max_time:
            return None

        robots = evolve(state.robots, ore=state.robots.ore + 1)
        return State(
            time=state.time + 1,
            stuff=state.stuff + state.robots - self.ore_cost,
            robots=robots,
        )

    def clay(self, max_time: int, state: State) -> State | None:
        while state.time < max_time and not state.stuff.matches(self.clay_cost):
            state = self.nothing(state)

        if state.time == max_time:
            return None

        robots = evolve(state.robots, clay=state.robots.clay + 1)
        return State(
            time=state.time + 1,
            stuff=state.stuff + state.robots - self.clay_cost,
            robots=robots,
        )

    def obsidian(self, max_time: int, state: State) -> State | None:
        while state.time < max_time and not state.stuff.matches(self.obsidian_cost):
            state = self.nothing(state)

        if state.time == max_time:
            return None

        robots = evolve(state.robots, obsidian=state.robots.obsidian + 1)
        return State(
            time=state.time + 1,
            stuff=state.stuff + state.robots - self.obsidian_cost,
            robots=robots,
        )

    def geode(self, max_time: int, state: State) -> State | None:
        while state.time < max_time and not state.stuff.matches(self.geode_cost):
            state = self.nothing(state)

        if state.time == max_time:
            return None

        robots = evolve(state.robots, geode=state.robots.geode + 1)
        return State(
            time=state.time + 1,
            stuff=state.stuff + state.robots - self.geode_cost,
            robots=robots,
        )

    def neighbours(self, max_time: int, state: State) -> list[State]:
        neighbours: list[State] = []

        # No point in producing something faster than you can spend it.
        if state.robots.ore < self.max_costs.ore:
            ore = self.ore(max_time, state)
            if ore is not None:
                neighbours.append(ore)

        if state.robots.clay < self.max_costs.clay:
            clay = self.clay(max_time, state)
            if clay is not None:
                neighbours.append(clay)

        if state.robots.obsidian < self.max_costs.obsidian:
            obsidian = self.obsidian(max_time, state)
            if obsidian is not None:
                neighbours.append(obsidian)

        geode = self.geode(max_time, state)
        if geode is not None:
            neighbours.append(geode)

        return neighbours

    def projection(self, max_time: int, state: State) -> int:
        remaining_time = max_time - state.time
        return state.stuff.geode + remaining_time * state.robots.geode

    def bound(self, max_time: int, state: State) -> int:
        # Pretend that we can produce everything all at once.
        time = state.time
        robots = state.robots
        stuffs = [state.stuff] * 4
        costs = [self.ore_cost, self.clay_cost, self.obsidian_cost, self.geode_cost]
        for _ in range(time, max_time):
            new_stuffs = []
            new_robots = []
            for stuff, cost in zip(stuffs, costs):
                stuff, robot = (stuff - cost, 1) if stuff.matches(cost) else (stuff, 0)
                new_stuffs.append(stuff)
                new_robots.append(robot)

            stuffs = [stuff + robots for stuff in new_stuffs]
            robots += Stuff(*new_robots)

        geode = stuffs[-1]
        return geode.geode

    def geode_production(self, max_time: int) -> int:
        start = State()
        best_production = 0
        stack = [start]
        seen: set[State] = set()
        while stack:
            state = stack.pop()
            if state in seen:
                continue
            seen.add(state)

            bound = self.bound(max_time, state)
            if bound <= best_production:
                continue

            projection = self.projection(max_time, state)
            if projection > best_production:
                best_production = projection

            if state.time < max_time:
                stack += self.neighbours(max_time, state)

        return best_production


def solve() -> None:
    input = data_dir() / "day19.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    blueprints = [Blueprint.from_line(line) for line in data.splitlines()]

    total = 0
    for index, blueprint in enumerate(blueprints, 1):
        geodes = blueprint.geode_production(24)
        total += index * geodes

    print(f"Part one: {total}")

    total = 1
    for blueprint in blueprints[:3]:
        geodes = blueprint.geode_production(32)
        total *= geodes

    print(f"Part two: {total}")
