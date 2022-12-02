from __future__ import annotations

from enum import Enum

from advent.utils import data_dir


class Result(Enum):
    WIN = 0
    LOSE = 1
    DRAW = 2


class Throw(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def stronger_throw(self) -> Throw:
        return Throw((self.value + 1) % 3)

    def weaker_throw(self) -> Throw:
        return Throw((self.value + 2) % 3)

    def result(self, other: Throw) -> Result:
        if self == other:
            return Result.DRAW

        if self.value % 3 == (other.value + 1) % 3:
            return Result.WIN

        return Result.LOSE


ABCStrategy = {
    "A": Throw.ROCK,
    "B": Throw.PAPER,
    "C": Throw.SCISSORS,
}

XYZStrategy1 = {
    "X": Throw.ROCK,
    "Y": Throw.PAPER,
    "Z": Throw.SCISSORS,
}

XYZStrategy2 = {
    "X": Throw.weaker_throw,
    "Y": lambda throw: throw,
    "Z": Throw.stronger_throw,
}


PlayScore = {
    Throw.ROCK: 1,
    Throw.PAPER: 2,
    Throw.SCISSORS: 3,
}

ResultScore = {
    Result.WIN: 6,
    Result.LOSE: 0,
    Result.DRAW: 3,
}


def game_score(mine: Throw, theirs: Throw) -> int:
    wld = mine.result(theirs)
    result_score = ResultScore[wld]
    play_score = PlayScore[mine]
    return result_score + play_score


def solve() -> None:
    input = data_dir() / "day02.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    score = 0
    for line in data.splitlines():
        abc, xyz = line.split(" ")
        their_throw = ABCStrategy[abc]
        my_throw = XYZStrategy1[xyz]
        score += game_score(my_throw, their_throw)

    print(f"Part one: {score}")

    score = 0
    for line in data.splitlines():
        abc, xyz = line.split(" ")
        their_throw = ABCStrategy[abc]
        my_throw = XYZStrategy2[xyz](their_throw)
        score += game_score(my_throw, their_throw)

    print(f"Part two: {score}")
