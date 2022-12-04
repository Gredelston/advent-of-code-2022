#!/usr/bin/env python3

import re


USE_SAMPLE = False


class SectionID(int):
    """A single section of the  camp, represented by an integer."""
    pass


class Elf:
    """A single elf, who is assigned a range of sections to clean."""
    def __init__(self, low: SectionID, high: SectionID):
        """Initialize the Elf with its (inclusive) range of sections.

        Args:
            low: The lowest sectionID that the elf is responsible for.
            high: The highest sectionID that the elf is responsible for.
        """
        self._low = low
        self._high = high

    @property
    def range(self) -> list[SectionID]:
        """Get a full list of this elf's assigned SectionIDs."""
        return [SectionID(i) for i in range(self._low, self._high + 1)]
    
    def contains(self, other: 'Elf') -> bool:
        """Check whether this elf's range completely contains another elf's."""
        return all([x in other.range for x in self.range])
    
    def completely_overlaps(self, other: 'Elf') -> bool:
        """Check whether this elf's range contains another, or vice-versa."""
        return self.contains(other) or other.contains(self)

    def overlaps_at_all(self, other: 'Elf') -> bool:
        """CHeck whether this elf's range completely overlaps another."""
        return any([x in other.range for x in self.range])


class ElfPair(tuple[Elf, Elf]):
    """A pair of elves who work together."""
    pass


def part1():
    """Solve and print the solution to part 1 of today's problem."""
    file_contents = load_file_contents()
    elf_pairs = create_elf_pairs(file_contents)
    print(count_full_overlaps(elf_pairs))


def create_elf_pairs(file_contents: list[str]) -> list[ElfPair]:
    """Interpret the file contents as pairs of elves."""
    elf_pairs: list[ElfPair] = []
    ELF_PAIR_REGEX = re.compile(r'^(\d+)-(\d+),(\d+)-(\d+)$')
    for line in file_contents:
        m = ELF_PAIR_REGEX.match(line)
        assert m is not None, f'Could not parse line: <{line}>'
        elf1 = Elf(SectionID(m.group(1)), SectionID(m.group(2)))
        elf2 = Elf(SectionID(m.group(3)), SectionID(m.group(4)))
        elf_pairs.append(ElfPair((elf1, elf2)))
    return elf_pairs


def count_full_overlaps(elf_pairs: list[ElfPair]) -> int:
    """Count how many pairs contain one elf which fully overlaps the other."""
    count = 0
    for elf_pair in elf_pairs:
        if elf_pair[0].completely_overlaps(elf_pair[1]):
            count += 1
    return count


def part2():
    """Solve and print the solution to part 1 of today's problem."""
    file_contents = load_file_contents()
    elf_pairs = create_elf_pairs(file_contents)
    print(count_all_overlaps(elf_pairs))


def count_all_overlaps(elf_pairs: list[ElfPair]) -> int:
    """Count how many pairs contain any overlapping sections."""
    count = 0
    for elf_pair in elf_pairs:
        if elf_pair[0].overlaps_at_all(elf_pair[1]):
            count += 1
    return count


def load_file_contents() -> list[str]:
    """Load the file contents."""
    fp = 'sample.txt' if USE_SAMPLE else 'input.txt'
    with open(fp) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


if __name__ == '__main__':
    part1()
    part2()
