from attrs import frozen

from advent.utils import data_dir


@frozen
class Map:
    rows: int
    columns: int
    trees: dict[tuple[int, int], int]

    def visible(self) -> set[tuple[int, int]]:
        visible = set()

        for row in range(self.rows):
            max = -1
            for column in range(self.columns):
                if self.trees[(row, column)] > max:
                    max = self.trees[(row, column)]
                    visible.add((row, column))

        for row in range(self.rows):
            max = -1
            for column in reversed(range(self.columns)):
                if self.trees[(row, column)] > max:
                    max = self.trees[(row, column)]
                    visible.add((row, column))

        for column in range(self.columns):
            max = -1
            for row in range(self.rows):
                if self.trees[(row, column)] > max:
                    max = self.trees[(row, column)]
                    visible.add((row, column))

        for column in range(self.columns):
            max = -1
            for row in reversed(range(self.rows)):
                if self.trees[(row, column)] > max:
                    max = self.trees[(row, column)]
                    visible.add((row, column))

        return visible

    def scenic_score(self, position: tuple[int, int]) -> int:
        start_height = self.trees[position]
        row, column = position

        up = 0
        for i in reversed(range(row)):
            up += 1
            if self.trees[(i, column)] >= start_height:
                break

        down = 0
        for i in range(row + 1, self.rows):
            down += 1
            if self.trees[(i, column)] >= start_height:
                break

        left = 0
        for j in reversed(range(column)):
            left += 1
            if self.trees[(row, j)] >= start_height:
                break

        right = 0
        for j in range(column + 1, self.columns):
            right += 1
            if self.trees[(row, j)] >= start_height:
                break

        return up * down * left * right


def solve() -> None:
    input = data_dir() / "day08.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    trees: dict[tuple[int, int], int] = {}
    for row, line in enumerate(data.splitlines()):
        for column, height in enumerate(line):
            trees[(row, column)] = int(height)

    rows = row + 1
    columns = column + 1
    map = Map(rows, columns, trees)

    print(f"Part one: {len(map.visible())}")

    max = 0
    for i in range(rows):
        for j in range(columns):
            score = map.scenic_score((i, j))
            if score > max:
                max = score

    print(f"Part two: {max}")
