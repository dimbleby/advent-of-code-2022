#!/usr/bin/env python3

from __future__ import annotations

import re

from attrs import frozen
from ortools.linear_solver import pywraplp

from advent.utils import data_dir

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3


@frozen
class Blueprint:
    costs: dict[tuple[int, int], int]

    @staticmethod
    def from_line(line: str) -> Blueprint:
        numbers = [int(number) for number in re.findall(r"(\d+)", line)]
        costs = {(i, j): 0 for i in range(4) for j in range(4)}
        costs[ORE, ORE] = numbers[1]
        costs[CLAY, ORE] = numbers[2]
        costs[OBSIDIAN, ORE] = numbers[3]
        costs[OBSIDIAN, CLAY] = numbers[4]
        costs[GEODE, ORE] = numbers[5]
        costs[GEODE, OBSIDIAN] = numbers[6]
        return Blueprint(costs)

    def geode_production(self, max_time: int) -> int:
        solver = pywraplp.Solver.CreateSolver("BOP")

        # Do we build robot i at time t?
        builds = {
            (i, t): solver.BoolVar(f"build_{i}_{t}")
            for i in range(4)
            for t in range(max_time + 1)
        }

        # How many of robot i are there at time t?
        bots = {
            (i, t): solver.IntVar(0, max_time, f"bots_{i}_{t}")
            for i in range(4)
            for t in range(max_time + 1)
        }

        # How much of stuff i do we have at time t?
        max_stuff = (max_time - 1) * max_time // 2
        stuff = {
            (i, t): solver.IntVar(0, max_stuff, f"stuff_{i}_{t}")
            for i in range(4)
            for t in range(max_time + 1)
        }

        # We start with no stuff, no builds, one ore robot.
        for i in range(4):
            solver.Add(stuff[i, 0] == 0)
            solver.Add(builds[i, 0] == 0)
            solver.Add(bots[i, 0] == (i == ORE))

        for t in range(1, max_time + 1):
            # Build at most one robot at a time.
            solver.Add(sum(builds[i, t] for i in range(4)) <= 1)

            for i in range(4):
                # Building a bot gives us a new bot.
                solver.Add(bots[i, t] == bots[i, t - 1] + builds[i, t])

                # To build some bot j, we must have had enough of stuff i.
                spends = [builds[j, t] * self.costs[j, i] for j in range(4)]
                for j in range(4):
                    solver.Add(stuff[i, t - 1] >= spends[j])

                # The amount of stuff we have is what we had before, plus what the bots
                # dug up, minus what we spent.
                solver.Add(
                    stuff[i, t] == stuff[i, t - 1] + bots[i, t - 1] - sum(spends)
                )

        # Maximize the number of geodes at the end.
        goal = stuff[GEODE, max_time]
        solver.Maximize(goal)

        status = solver.Solve()
        assert status == pywraplp.Solver.OPTIMAL

        geodes = solver.Objective().Value()
        return int(geodes)


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


if __name__ == "__main__":
    solve()
