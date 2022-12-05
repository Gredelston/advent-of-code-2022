#!/usr/bin/env python3

import re
from typing import Optional


class Crate(str):
    """A crate, which is identified by a name (normally one char long)."""
    pass


class Stack(list[Crate]):
    """A stack of crates. Good for append() and pop()."""
    def __init__(self, crates: list[Crate]):
        self._crates = crates

    def pop(self) -> Crate:
        return self._crates.pop()

    def append(self, crate: Crate):
        self._crates.append(crate)

    def extend(self, crates: list[Crate]):
        self._crates.extend(crates)

    def pop_multiple(self, quantity: int):
        """Pop multiple crates off the stack, maintaining their order."""
        popped = self._crates[-quantity:]
        self._crates = self._crates[:-quantity]
        return popped


class Crane:
    """A fancy machine that can move crates from stack to stack.

    Args:
        stacks: The stacks that this crane can operate on, from left to right.
    """
    def __init__(self, stacks: list[Stack]):
        self._stacks = stacks

    def _get_stack(self, stack_number: int) -> Stack:
        """Return the stack referenced by its 1-indexed ID number."""
        return self._stacks[stack_number - 1]

    def move_crate(self, from_stack: Stack, to_stack: Stack):
        """Move a single crate from one stack to another."""
        crate = from_stack.pop()
        to_stack.append(crate)

    def move_crates_together(self, from_stack: Stack, to_stack: Stack,
            quantity: int):
        """Move several crates from one stack to another."""
        crates = from_stack.pop_multiple(quantity)
        to_stack.extend(crates)

    
    def perform_procedure(self, file_contents: list[str],
            move_together: bool = False):
        started_instructions = False
        for line in file_contents:
            if not line:
                started_instructions = True
                continue
            if not started_instructions:
                continue
            m = re.match(r'^move (\d+) from (\d+) to (\d+)$', line)
            assert m is not None, line
            quantity = int(m.group(1))
            from_stack = self._get_stack(int(m.group(2)))
            to_stack = self._get_stack(int(m.group(3)))
            if move_together:
                self.move_crates_together(from_stack, to_stack, quantity)
            else:
                for _ in range(quantity):
                    self.move_crate(from_stack, to_stack)

    def read_stacks(self) -> str:
        message = ''
        for stack in self._stacks:
            message += stack.pop()
        return message


def part1(use_sample: bool = False) -> None:
    """Solve part 1 of today's problem."""
    file_contents = load_file_contents(use_sample)
    stacks = FileParser(file_contents).initialize_stacks()
    crane = Crane(stacks)
    crane.perform_procedure(file_contents)
    return crane.read_stacks()


def part2(use_sample: bool = False) -> None:
    """Solve part 1 of today's problem."""
    file_contents = load_file_contents(use_sample)
    stacks = FileParser(file_contents).initialize_stacks()
    crane = Crane(stacks)
    crane.perform_procedure(file_contents, move_together=True)
    return crane.read_stacks()


def load_file_contents(use_sample: bool) -> list[str]:
    """Load the input file to strings.

    Args:
        use_sample: Option to use the sample input instead of the real input.
    """
    fp = 'sample.txt' if use_sample else 'input.txt'
    with open(fp) as f:
        lines = f.readlines()
    return [line.strip('\n') for line in lines]


class FileParser:
    def __init__(self, file_contents: list[str]):
        self._contents = file_contents
        self._stack_id_line_no: Optional[int] = None

    def initialize_stacks(self) -> list[Stack]:
        stacks: list[Stack] = []
        for _ in range(self.number_of_stacks):
            stacks.append(Stack([]))
        for line in self._contents[:self.stack_id_line_no][::-1]:
            for column_number, char in enumerate(line):
                if not char.isalpha():
                    continue
                crate = Crate(char)
                stack_number = int(self.stack_id_line[column_number])
                stacks[stack_number - 1].append(crate)
        return stacks


    @property
    def stack_id_line_no(self) -> int:
        """Return the line number containing the stack ID line."""
        if self._stack_id_line_no is None:
            for i, line in enumerate(self._contents):
                if all(s.isnumeric() for s in line.strip().split()):
                    self._stack_id_line_no = i
                    break
            if self._stack_id_line_no is None:
                raise Exception('Failed to find a stack ID line.')
        return self._stack_id_line_no

    @property
    def stack_id_line(self) -> str:
        return self._contents[self.stack_id_line_no]

    @property
    def number_of_stacks(self) -> int:
        return int(self.stack_id_line.split()[-1])


def initialize_stacks(file_contents):
    stack_id_line = get_stack_id_line(file_contents)
    num_stacks = count_stacks(file_contents)


if __name__ == '__main__':
    print('Samples:')
    print(f'\tPart 1: {part1(True)}')
    print(f'\tPart 2: {part2(True)}')
    print('Real input:')
    print(f'\tPart 1: {part1(False)}')
    print(f'\tPart 2: {part2(False)}')
