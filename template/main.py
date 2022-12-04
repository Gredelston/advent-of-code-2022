#!/usr/bin/env python3

USE_SAMPLE = True


def part1():
    """Solve and print the solution to part 1 of today's problem."""
    file_contents = load_file_contents()


def part2():
    """Solve and print the solution to part 1 of today's problem."""
    file_contents = load_file_contents()


def load_file_contents() -> list[str]:
    fp = 'sample.txt' if USE_SAMPLE else 'input.txt'
    with open(fp) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


if __name__ == '__main__':
    part1()
    part2()
