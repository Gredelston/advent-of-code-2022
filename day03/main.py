#!/usr/bin/env python3

USE_SAMPLE = False


class Item(str):
    """A single item in an elf's rucksack. Should be exactly one character."""
    @property
    def priority(self):
        """Get the priority of the item."""
        CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        assert self in CHARS, self
        return CHARS.index(self) + 1


class Compartment:
    """A compartment of a rucksack, which contains some items."""
    def __init__(self, items: set[Item]):
        """Set up the compartment with some items."""
        self._items = items

    @property
    def items(self):
        """Public accessor for the compartment's items."""
        return self._items

    def find_overlap_with(self, other: 'Compartment') -> Item:
        """Find the single item which is shared with another Compartment."""
        overlap: set[Item] = self.items & other.items
        assert len(overlap) == 1, f'{self.items} & {other.items} = {overlap}'
        return overlap.pop()


class Rucksack:
    """A rucksack, which contains some items."""
    def __init__(self, items: list[Item]):
        """Set up the rucksack with an even number of items."""
        self._items = items
        assert not len(self._items) % 2

    @property
    def items_set(self) -> set[Item]:
        """Get a set of the compartment's unique items."""
        return set(self._items)

    @property
    def compartments(self) -> tuple[Compartment, Compartment]:
        """Access the two compartments in the rucksack."""
        half_length = int(len(self) / 2)
        compartment1_items = self._items[:half_length]
        compartment1 = Compartment(set(compartment1_items))
        compartment2_items = self._items[half_length:]
        compartment2 = Compartment(set(compartment2_items))
        return (compartment1, compartment2)
    
    def find_wrong_item(self) -> Item:
        """Find the item which is in both of this rucksack's compartments."""
        comp1, comp2 = self.compartments
        return comp1.find_overlap_with(comp2)

    def find_badge(self, other1: 'Rucksack', other2: 'Rucksack') -> Item:
        """Find the only item which is in this and two other rucksacks."""
        overlap = self.items_set & other1.items_set & other2.items_set
        assert len(overlap) == 1
        return overlap.pop()

    def __len__(self):
        """The number of items in the rucksack."""
        return len(self._items)

    def __repr__(self):
        """Pretty-print the rucksack for debugging."""
        return f'Rucksack<{self._items}>'


def part1():
    """Part 1: Find the priorities of each rucksack's shared item."""
    file_contents = load_file_contents()
    rucksacks = get_rucksacks(file_contents)
    print(sum(rucksack.find_wrong_item().priority for rucksack in rucksacks))


def load_file_contents() -> list[str]:
    """Load the input file."""
    fp: str = 'sample.txt' if USE_SAMPLE else 'input.txt'
    with open(fp) as f:
        lines: list[str] = f.readlines()
    return [line.strip() for line in lines]


def get_rucksacks(file_contents):
    """Process the file contents into a list of rucksacks."""
    rucksacks = []
    for line in file_contents:
        items = [Item(char) for char in line]
        rucksacks.append(Rucksack(items))
    return rucksacks


def part2():
    """Part 2: Find the priorities of each elf group's badge."""
    file_contents = load_file_contents()
    rucksacks = get_rucksacks(file_contents)
    score = 0
    for i in range(int(len(rucksacks) / 3)):
        r1, r2, r3 = rucksacks[3*i:3*i+3]
        score += r1.find_badge(r2, r3).priority
    print(score)


if __name__ == '__main__':
    part1()
    part2()
