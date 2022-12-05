import itertools

from attrs import frozen

from advent.utils import data_dir

START = [
    ["Z", "P", "M", "H", "R"],
    ["P", "C", "J", "B"],
    ["S", "N", "H", "G", "L", "C", "D"],
    ["F", "T", "M", "D", "Q", "S", "R", "L"],
    ["F", "S", "P", "Q", "B", "T", "Z", "M"],
    ["T", "F", "S", "Z", "B", "G"],
    ["N", "R", "V"],
    ["P", "G", "L", "T", "D", "V", "C", "M"],
    ["W", "Q", "N", "J", "F", "M", "L"],
]


@frozen
class Move:
    count: int
    from_: int
    to: int


def solve() -> None:
    input = data_dir() / "day05.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()
    lines = data.splitlines()

    # Skip over the starting configuration, that's done by hand (above).
    moves: list[Move] = []
    for line in itertools.dropwhile(lambda line: line != "", lines):
        if not line:
            continue

        words = line.split(" ")
        count, from_, to = int(words[1]), int(words[3]), int(words[5])
        move = Move(count, from_, to)
        moves.append(move)

    stacks = [stack[:] for stack in START]
    for move in moves:
        from_stack = stacks[move.from_ - 1]
        to_stack = stacks[move.to - 1]
        for _ in range(move.count):
            crate = from_stack.pop()
            to_stack.append(crate)

    part_one = "".join(stack[-1] for stack in stacks)
    print(f"Part one: {part_one}")

    stacks = [stack[:] for stack in START]
    for move in moves:
        from_stack = stacks[move.from_ - 1]
        to_stack = stacks[move.to - 1]
        moved = from_stack[-move.count :]
        stacks[move.from_ - 1] = from_stack[: -move.count]
        to_stack += moved

    part_two = "".join(stack[-1] for stack in stacks)
    print(f"Part two: {part_two}")
