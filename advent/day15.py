from __future__ import annotations

import re

from attrs import Factory, define, frozen

from advent.utils import data_dir


@frozen
class Cell:
    x: int
    y: int

    def manhattan(self, other: Cell) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@frozen
class Range:
    # lo <= n < hi
    lo: int
    hi: int

    def size(self) -> int:
        return self.hi - self.lo

    def touches(self, other: Range) -> bool:
        return self.lo <= other.hi and self.hi >= other.lo


@define
class RangeUnion:
    # Non-overlapping
    ranges: set[Range] = Factory(set)

    def add(self, new_range: Range) -> None:
        ranges: set[Range] = set()
        lo, hi = new_range.lo, new_range.hi
        for old_range in self.ranges:
            if old_range.touches(new_range):
                lo = min(lo, old_range.lo)
                hi = max(hi, old_range.hi)
            else:
                ranges.add(old_range)

        ranges.add(Range(lo, hi))
        self.ranges = ranges

    def size(self) -> int:
        return sum(r.size() for r in self.ranges)

    def intersect(self, other: Range) -> None:
        ranges: set[Range] = set()
        for old_range in self.ranges:
            if old_range.hi < other.lo:
                continue

            if old_range.lo > other.hi:
                continue

            lo = max(old_range.lo, other.lo)
            hi = min(old_range.hi, other.hi)
            ranges.add(Range(lo, hi))

        self.ranges = ranges

    def gap(self) -> int | None:
        if len(self.ranges) != 2:
            return None

        this, that = list(self.ranges)
        if this.hi + 1 == that.lo:
            return this.hi

        if that.hi + 1 == this.lo:
            return that.hi

        raise AssertionError


def solve() -> None:
    input = data_dir() / "day15.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    facts: list[tuple[Cell, Cell]] = []
    for line in data.splitlines():
        [sx, sy, bx, by] = re.findall(r"(-?\d+)", line)
        sensor = Cell(int(sx), int(sy))
        beacon = Cell(int(bx), int(by))
        facts.append((sensor, beacon))

    visible = RangeUnion()
    row = 2000000
    for sensor, beacon in facts:
        beaker_distance = sensor.manhattan(beacon)
        row_distance = abs(sensor.y - row)
        spare_range = beaker_distance - row_distance
        if spare_range <= 0:
            continue

        lo = sensor.x - spare_range
        hi = sensor.x + spare_range

        # Exclude the beacons themselves in part one.
        if beacon.x == lo:
            lo += 1
        if beacon.x == hi:
            hi -= 1

        visible.add(Range(lo, hi + 1))

    print(f"Part one: {visible.size()}")

    for row in range(4000001):
        visible = RangeUnion()
        for sensor, beacon in facts:
            beaker_distance = sensor.manhattan(beacon)
            row_distance = abs(sensor.y - row)
            spare_range = beaker_distance - row_distance
            if spare_range < 0:
                continue

            lo = sensor.x - spare_range
            hi = sensor.x + spare_range
            visible.add(Range(lo, hi + 1))

        visible.intersect(Range(0, 4000001))
        gap = visible.gap()
        if gap is not None:
            print(f"Part two: {4000000 * gap + row}")
            break
