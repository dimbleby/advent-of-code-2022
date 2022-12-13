from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import frozen

from advent.utils import chunks, data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator


@frozen(order=False)
class Packet:
    subpackets: list[int | Packet]

    @staticmethod
    def from_text(letters: Iterator[str]) -> Packet:
        subpackets: list[int | Packet] = []

        number = None
        while True:
            letter = next(letters, None)

            if letter is None or letter == "]":
                if number is not None:
                    subpackets.append(number)
                return Packet(subpackets)

            if letter == ",":
                if number is not None:
                    subpackets.append(number)
                number = None
                continue

            if letter == "[":
                subpacket = Packet.from_text(letters)
                subpackets.append(subpacket)
                continue

            if number is None:
                number = 0
            number *= 10
            number += int(letter)

    def cmp(self, other: Packet) -> int:
        for left, right in zip(self.subpackets, other.subpackets):
            if isinstance(left, int) and isinstance(right, int):
                if left < right:
                    return -1
                if left > right:
                    return 1

            else:
                subl = Packet([left]) if isinstance(left, int) else left
                subr = Packet([right]) if isinstance(right, int) else right
                inner = subl.cmp(subr)
                if inner != 0:
                    return inner

        if len(self.subpackets) < len(other.subpackets):
            return -1

        if len(self.subpackets) > len(other.subpackets):
            return 1

        return 0

    def __lt__(self, other: Packet) -> bool:
        return self.cmp(other) == -1


def solve() -> None:
    input = data_dir() / "day13.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    packets: list[Packet] = []
    for line in data.splitlines():
        if not line:
            continue

        letters = iter(line)
        next(letters)
        packet = Packet.from_text(letters)
        packets.append(packet)

    total = 0
    for index, pair in enumerate(chunks(packets, 2), 1):
        if pair[0] < pair[1]:
            total += index

    print(f"Part one: {total}")

    dividers = (Packet([Packet([2])]), Packet([Packet([6])]))
    packets += dividers
    packets.sort()
    idx1 = packets.index(dividers[0])
    idx2 = packets.index(dividers[1])
    print(f"Part two: {(idx1 + 1) * (idx2 + 1)}")
