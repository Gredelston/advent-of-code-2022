#!/usr/bin/env python3


def part1(use_sample: bool = False) -> None:
    """Solve part 1 of today's problem."""
    file_contents = load_file_contents(use_sample)


def part2(use_sample: bool = False) -> None:
    """Solve part 2 of today's problem."""
    file_contents = load_file_contents(use_sample)


def load_file_contents(use_sample: bool) -> list[str]:
    """Load the input file to strings.

    Args:
        use_sample: Option to use the sample input instead of the real input.
    """
    fp = 'sample.txt' if use_sample else 'input.txt'
    with open(fp) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


if __name__ == '__main__':
    print('Samples:')
    print(f'\tPart 1: {part1(True)}')
    print(f'\tPart 2: {part2(True)}')
    print('Real input:')
    print(f'\tPart 1: {part1(False)}')
    print(f'\tPart 2: {part2(False)}')
