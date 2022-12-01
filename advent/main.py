#!/usr/bin/env python3

import importlib
import sys


def main() -> None:
    day = int(sys.argv[1])
    module = importlib.import_module(f"advent.day{day:02}")
    module.solve()


if __name__ == "__main__":
    main()
