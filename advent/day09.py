from attrs import frozen

from advent.utils import data_dir


def sign(n: int) -> int:
    if n == 0:
        return 0

    return n // abs(n)


@frozen
class Position:
    x: int
    y: int


MOVEMENT = {
    "U": (0, 1),
    "D": (0, -1),
    "R": (1, 0),
    "L": (-1, 0),
}


class Rope:
    def __init__(self, count: int) -> None:
        self.knots = [Position(0, 0)] * count

    def move(self, direction: str) -> None:
        dx, dy = MOVEMENT[direction]
        head = self.knots[0]
        self.knots[0] = Position(x=head.x + dx, y=head.y + dy)

        for knot in range(1, len(self.knots)):
            self.update_knot(knot)

    def update_knot(self, n: int) -> None:
        leader = self.knots[n - 1]
        follower = self.knots[n]

        if abs(leader.x - follower.x) <= 1 and abs(leader.y - follower.y) <= 1:
            return

        dx = sign(leader.x - follower.x)
        dy = sign(leader.y - follower.y)

        self.knots[n] = Position(x=follower.x + dx, y=follower.y + dy)


def solve() -> None:
    input = data_dir() / "day09.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    rope = Rope(2)
    visited = {rope.knots[-1]}

    for line in data.splitlines():
        direction, count = line.split(" ")
        for _ in range(int(count)):
            rope.move(direction)
            visited.add(rope.knots[-1])

    print(f"Part one: {len(visited)}")

    rope = Rope(10)
    visited = {rope.knots[-1]}

    for line in data.splitlines():
        direction, count = line.split(" ")
        for _ in range(int(count)):
            rope.move(direction)
            visited.add(rope.knots[-1])

    print(f"Part two: {len(visited)}")
