from typing import Sequence

from advent.utils import data_dir

KEY = 811589153


def mix(input: Sequence[int]) -> list[int]:
    uniqued = list(enumerate(input))
    length = len(input) - 1
    for item in enumerate(input):
        position = uniqued.index(item)
        uniqued.pop(position)
        new_position = (position + item[1] - 1) % length + 1
        uniqued.insert(new_position, item)

    return [value for _, value in uniqued]


def mix2(input: Sequence[int]) -> list[int]:
    uniqued = list(enumerate(input))
    for _ in range(10):
        length = len(input) - 1
        for item in enumerate(input):
            position = uniqued.index(item)
            uniqued.pop(position)
            new_position = (position + KEY * item[1] - 1) % length + 1
            uniqued.insert(new_position, item)

    return [KEY * value for _, value in uniqued]


def extract_sum(input: Sequence[int]) -> int:
    length = len(input)
    zero = input.index(0)
    indices = [(zero + n) % length for n in (1000, 2000, 3000)]
    total = sum(input[index] for index in indices)
    return total


def solve() -> None:
    input = data_dir() / "day20.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    numbers = [int(line) for line in data.splitlines()]

    output = mix(numbers)
    answer = extract_sum(output)
    print(f"Part one: {answer}")

    output = mix2(numbers)
    answer = extract_sum(output)
    print(f"Part two: {answer}")
