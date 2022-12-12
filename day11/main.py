#!/usr/bin/env python3

from collections.abc import Callable
import re
import typing

DEBUG = True

def _debug(msg, *args, **kwargs):
    if DEBUG:
        print(msg, *args, **kwargs)


class Item(int):
    pass


class MonkeyID(int):
    pass


Operation = typing.NewType('Operation', Callable[[Item], Item])
ItemTest = typing.NewType('ItemTest', Callable[[Item], bool])


class ChunkToMonkeyInterpreter(list[str]):
    _MONKEY_ID_LINE_NO = 0
    _STARTING_ITEMS_LINE_NO = 1
    _OPERATION_LINE_NO = 2
    _TEST_LINE_NO = 3
    _IF_TRUE_LINE_NO = 4
    _IF_FALSE_LINE_NO = 5

    def _line(self, line_number: int) -> str:
        return self[line_number]

    def _get_id(self) -> int:
        line = self._line(self._MONKEY_ID_LINE_NO)
        m = re.match(r'Monkey (\d+):$', line)
        return m.group(1)

    def _get_starting_items(self) -> list[Item]:
        line = self._line(self._STARTING_ITEMS_LINE_NO)
        m = re.match(r'^\s*Starting items: (\d+(, \d+)*)$', line)
        assert m, line
        raw_items = m.group(1)
        return [Item(element) for element in raw_items.split(', ')]

    def _get_operation(self) -> Operation:
        line = self._line(self._OPERATION_LINE_NO)
        m = re.match(r'^\s*Operation: new = old ([+*]) ((old)|(\d+))$', line)
        operator = m.group(1)
        second_operand_raw = m.group(2)
        def operation(old_value: Item) -> Item:
            second_operand: int
            second_operand_message: str
            if second_operand_raw == 'old':
                second_operand = old_value
                second_operand_message = 'itself'
            else:
                second_operand = int(second_operand_raw)
                second_operand_message = str(second_operand)
            if operator == '+':
                operator_message = 'increases'
                new_value = old_value + second_operand
            elif operator == '*':
                operator_message = 'is multiplied'
                new_value = old_value * second_operand
            else:
                raise ValueError(f'Unexpected operator: {operator}')
            message = f'    Worry level {operator_message} by ' \
                      f'{second_operand_message} to {new_value}.'
            _debug(message)
            return Item(new_value)
        return Operation(operation)

    def _get_test(self) -> ItemTest:
        line = self._line(self._TEST_LINE_NO)
        m = re.match(r'Test: divisible by (\d+)', line)
        divisor = int(m.group(1))
        def item_test(item: Item) -> bool:
            is_divisible = item % divisor == 0
            if is_divisible:
                _debug(f'    Current worry level is divisible by {divisor}.')
            else:
                _debug(f'    Current worry level is not divisible by '
                       f'{divisor}.')
            return is_divisible
        return ItemTest(item_test)

    def _get_if_true_destination(self) -> MonkeyID:
        line = self._line(self._IF_TRUE_LINE_NO)
        m = re.match(r'^\s*If true: throw to monkey (\d+)$', line)
        return MonkeyID(m.group(1))

    def _get_if_false_destination(self) -> MonkeyID:
        line = self._line(self._IF_FALSE_LINE_NO)
        m = re.match(r'^\s*If false: throw to monkey (\d+)$', line)
        return MonkeyID(m.group(1))


class Monkey:
    def __init__(self, file_chunk: list[str], monkey_club: 'MonkeyClub'):
        self._monkey_club = monkey_club
        self.inspections_count = 0

        chunk_interpreter = ChunkToMonkeyInterpreter(file_chunk)
        self._id: MonkeyID = chunk_interpreter._get_id()
        self._items: list[Item] = chunk_interpreter._get_starting_items()
        self._operation: Operation = chunk_interpreter._get_operation()
        self._test: [Item] = chunk_interpreter._get_test()
        self._true_destination: MonkeyID = \
                chunk_interpreter._get_if_true_destination()
        self._false_destination: MonkeyID = \
                chunk_interpreter._get_if_false_destination()

    def execute_round(self):
        _debug(f'Monkey {self._id}:')
        for item in self._items:
            self._inspect(item)
        self._items: list[Item] = []

    def _inspect(self, item: Item):
        self.inspections_count += 1
        _debug(f'  Monkey inspects an item with a worry level of {item}.')
        item = self._operation(item)
        item = Item(item/3)
        _debug('    Monkey gets bored with item. Worry level is divided by 3 '
               f'to {item}.')
        test_passed = self._test(item)
        to_monkey_id: MonkeyID
        if test_passed:
            to_monkey_id = self._true_destination
        else:
            to_monkey_id = self._false_destination
        _debug(f'    Item with worry level {item} is thrown to monkey '
               f'{to_monkey_id}.')
        self._monkey_club.get_monkey(to_monkey_id).add_item(item)

    def add_item(self, item: Item):
        self._items.append(item)

    def __str__(self) -> str:
        return f'Monkey {self._id}: {", ".join(str(i) for i in self._items)}'



class MonkeyClub:
    def __init__(self, monkeys: list[Monkey] = []):
        self._monkeys = monkeys

    def add_monkey(self, new_monkey: Monkey):
        self._monkeys.append(new_monkey)

    def get_monkey(self, index: int) -> Monkey:
        return self._monkeys[index]

    def execute_round(self, round_number: int=-1):
        print()
        print(f'Beginning round {round_number}')
        print()
        for monkey in self._monkeys:
            monkey.execute_round()
        _debug(f'After round {round_number}, the monkeys are holding items '
                'with these worry levels:')
        for monkey in self._monkeys:
            _debug(str(monkey))

    def get_monkey_business(self) -> int:
        inspections_per_monkey = [
                monkey.inspections_count for monkey in self._monkeys]
        print(inspections_per_monkey)
        inspections_per_monkey.sort()
        return inspections_per_monkey[-1] * inspections_per_monkey[-2]

def part1(use_sample: bool = False) -> int:
    """Solve part 1 of today's problem."""
    file_chunks = load_file_chunks(use_sample)
    monkey_club = initialize_monkey_club(file_chunks)
    for round_number in range(1, 21):
        monkey_club.execute_round(round_number)
    return monkey_club.get_monkey_business()


def part2(use_sample: bool = False) -> None:
    """Solve part 2 of today's problem."""
    file_contents = load_file_chunks(use_sample)


def load_file_chunks(use_sample: bool) -> list[list[str]]:
    """Load the input file to lists of strings, separated by blank lines.

    Args:
        use_sample: Option to use the sample input instead of the real input.
    """
    fp = 'sample.txt' if use_sample else 'input.txt'
    with open(fp) as f:
        lines = f.readlines()
    chunks: list[list[str]] = []
    new_chunk: list[str] = []
    for i, line in enumerate(lines):
        if line.strip():
            new_chunk.append(line.strip())
        else:
            chunks.append(new_chunk)
            new_chunk: list[str] = []
    assert new_chunk == []
    return chunks


def initialize_monkey_club(file_chunks: list[list[str]]) -> MonkeyClub:
    monkey_club = MonkeyClub()
    for chunk in file_chunks:
        monkey_club.add_monkey(Monkey(chunk, monkey_club))
    return monkey_club


if __name__ == '__main__':
    print('Samples:')
    print(f'\tPart 1: {part1(True)}')
    #print(f'\tPart 2: {part2(True)}')
    print('Real input:')
    print(f'\tPart 1: {part1(False)}')
    #print(f'\tPart 2: {part2(False)}')
