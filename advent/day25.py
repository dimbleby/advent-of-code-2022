from advent.utils import data_dir


def from_snafu(snafu: str) -> int:
    value = 0
    for char in snafu:
        value *= 5
        match char:
            case "-":
                value -= 1

            case "=":
                value -= 2

            case d:
                value += int(d)

    return value


def to_snafu(value: int) -> str:
    chars: list[str] = []
    while value != 0:
        match value % 5:
            case 4:
                char = "-"
                value += 5

            case 3:
                char = "="
                value += 5

            case n:
                char = str(n)

        chars.append(char)
        value //= 5

    chars.reverse()
    return "".join(chars)


def solve() -> None:
    input = data_dir() / "day25.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    values = [from_snafu(line) for line in data.splitlines()]
    total = sum(values)
    answer = to_snafu(total)

    print(f"Part one: {answer}")
