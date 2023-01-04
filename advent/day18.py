from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, TypeAlias

from advent.utils import data_dir

if TYPE_CHECKING:
    from collections.abc import Iterable

Cube: TypeAlias = tuple[int, int, int]

NEIGHBOURS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


def cube_from_line(line: str) -> Cube:
    x, y, z = line.split(",")
    return (int(x), int(y), int(z))


def surface_area(cubes: Iterable[Cube]) -> int:
    placed: set[Cube] = set()
    faces = 0
    for x, y, z in cubes:
        faces += 6

        for dx, dy, dz in NEIGHBOURS:
            if (x + dx, y + dy, z + dz) in placed:
                faces -= 2

        placed.add((x, y, z))

    return faces


def solve() -> None:
    input = data_dir() / "day18.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    lava = {cube_from_line(line) for line in data.splitlines()}

    area = surface_area(lava)

    print(f"Part one: {area}")

    # Fill a cube surrounding the lava.
    minx = min(x for x, y, z in lava) - 1
    maxx = max(x for x, y, z in lava) + 1
    miny = min(y for x, y, z in lava) - 1
    maxy = max(y for x, y, z in lava) + 1
    minz = min(z for x, y, z in lava) - 1
    maxz = max(z for x, y, z in lava) + 1

    start = (minx, miny, minz)
    steam: set[Cube] = set()
    queue = deque([start])
    while queue:
        cube = queue.popleft()
        if cube in steam:
            continue

        steam.add(cube)

        x, y, z = cube
        for dx, dy, dz in NEIGHBOURS:
            x2, y2, z2 = x + dx, y + dy, z + dz
            if not minx <= x2 <= maxx:
                continue
            if not miny <= y2 <= maxy:
                continue
            if not minz <= z2 <= maxz:
                continue
            if (x2, y2, z2) in lava:
                continue

            queue.append((x2, y2, z2))

    steam_area = surface_area(steam)

    # Discount the outer surface of the steam cube.
    xlen = maxx - minx + 1
    ylen = maxy - miny + 1
    zlen = maxz - minz + 1
    cube_area = 2 * ((xlen * ylen) + (ylen * zlen) + (zlen * xlen))

    print(f"Part two: {steam_area - cube_area}")
