from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import frozen

from advent.utils import data_dir

if TYPE_CHECKING:
    from collections.abc import Iterator


@frozen
class File:
    name: str
    size: int


@frozen
class Directory:
    name: str
    files: list[File]
    subdirs: list[Directory]
    size: int

    @staticmethod
    def from_commands(name: str, commands: Iterator[str]) -> Directory:
        files: list[File] = []
        subdirs: list[Directory] = []
        size = 0

        while True:
            command = next(commands, None)

            # No more commands or changing up a directory completes this directory.
            if command is None or command == "$ cd ..":
                return Directory(name, files, subdirs, size)

            # We only need to pay attention to cd commands and file listings.
            if command.startswith("dir") or command.startswith("$ ls"):
                continue

            # Changing into a directory creates a new subdirectory.
            words = command.split(" ")
            if command.startswith("$ cd"):
                subdir = Directory.from_commands(words[2], commands)
                subdirs.append(subdir)
                size += subdir.size
                continue

            # Else we have a file.
            file = File(words[1], int(words[0]))
            files.append(file)
            size += file.size


def solve() -> None:
    input = data_dir() / "day07.txt"
    with open(input, encoding="utf-8") as f:
        data = f.read()

    lines = data.splitlines()
    commands = iter(lines)

    # Skip the opening "cd /"
    next(commands)
    root = Directory.from_commands("/", commands)

    total = 0
    stack = [root]
    while stack:
        directory = stack.pop()
        if directory.size <= 100000:
            total += directory.size
        stack += directory.subdirs

    print(f"Part one: {total}")

    available = 70000000 - root.size
    needed = 30000000 - available
    best_size = root.size
    stack = [root]
    while stack:
        directory = stack.pop()
        if directory.size >= needed and directory.size < best_size:
            best_size = directory.size
        stack += directory.subdirs

    print(f"Part two: {best_size}")
