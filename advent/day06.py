from advent.utils import data_dir


def all_different(chars: str) -> bool:
    return len(chars) == len(set(chars))


def solve() -> None:
    input = data_dir() / "day06.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    for index in range(len(data)):
        if all_different(data[index : index + 4]):
            print(f"Part one: {index + 4}")
            break

    for index in range(len(data)):
        if all_different(data[index : index + 14]):
            print(f"Part two: {index + 14}")
            break
