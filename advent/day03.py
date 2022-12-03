from advent.utils import chunks, data_dir


def priority(letter: str) -> int:
    lowered = letter.lower()
    priority = ord(lowered) - ord("a") + 1

    if letter.isupper():
        priority += 26

    return priority


def solve() -> None:
    input = data_dir() / "day03.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    lines = data.splitlines()

    total = 0
    for line in lines:
        halfway = len(line) // 2
        compartment_one = line[:halfway]
        compartment_two = line[halfway:]
        common = set(compartment_one) & set(compartment_two)
        item = common.pop()
        total += priority(item)

    print(f"Part one: {total}")

    total = 0
    for group in chunks(lines, 3):
        sets = (set(items) for items in group)
        common = set.intersection(*sets)
        badge = common.pop()
        total += priority(badge)

    print(f"Part two: {total}")
