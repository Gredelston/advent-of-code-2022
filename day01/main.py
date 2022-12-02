#!/usr/bin/env python3

"""Solve Advent of Code 2022, day 1... with no function longer than one line."""

# pylint: disable=too-few-public-methods

from abc import ABC
from dataclasses import dataclass


class Calories(int):
    """A quantity of calories."""


@dataclass
class Food:
    """A food which can be carried by an elf. Contains some calories."""
    calories: Calories


class Elf:
    """A single elf, who carries some foods."""
    def __init__(self, foods: list[Food]):
        """Initialize the elf with their foods.

        Args:
            foods: The foods carried by the elf.
        """
        self._foods = foods

    def get_total_calories(self) -> Calories:
        """Find the total number of calories carried by the elf."""
        return Calories(sum([food.calories for food in self._foods]))

    @staticmethod
    def read_total_calories(elf: 'Elf') -> Calories:
        """Read the total number of calories carried by some elf.

        Args:
            elf: The elf whose calories should be read.
        """
        return elf.get_total_calories()

    def __repr__(self) -> str:
        """Print info about the elf for debugging purposes."""
        return f'Elf<{self.get_total_calories()}>'


class MultipleElves:
    """Class to represent an unordered collection of elves."""
    def __init__(self, elves: list[Elf]):
        """Initialize the elves.

        Args:
            elves: An unordered collection of elves.
        """
        self._elves = elves

    def _get_elves_sorted_by_calories(self) -> list[Elf]:
        """Return the inner elves, sorted from fewest to most calories."""
        return sorted(self._elves, key=Elf.read_total_calories)

    def get_elf_with_most_calories(self) -> Elf:
        """Find the single elf carrying the most calories."""
        return self._get_elves_sorted_by_calories()[-1]

    def get_n_elves_with_most_calories(self, num_elves: int) -> 'MultipleElves':
        """Find the n elves carrying the most calories.

        Args:
            num_elves: The number of elves to search for.
        """
        return MultipleElves(self._get_elves_sorted_by_calories()[-num_elves:])

    def get_total_calories(self) -> Calories:
        """Find the total number of calories carried by all contained elves."""
        return sum((elf.get_total_calories() for elf in self._elves),
                start=Calories(0))

    def __len__(self) -> int:
        """Find the number of elves in this collection."""
        return len(self._elves)

    def __repr__(self) -> str:
        """Print info about the elves for debugging purposes."""
        return f'MultipleElves<[{self._elves}]>'


class ProblemSolution(ABC):
    """Abstract class representing a solution to a single problem."""
    _problem_number: int = -1

    def __init__(self, value: Calories):
        """Initialize the solution.

        Args:
            value: The value of the solution, to be entered on the AOC site.
        """
        self._value = value

    def print(self):
        """Pretty-print the solution."""
        print(f'Problem #{self._problem_number}: {self._value}')


class ProblemOneSolution(ProblemSolution):
    """Class for the solution to Problem #1."""
    _problem_number = 1


class ProblemTwoSolution(ProblemSolution):
    """Class for the solution to Problem #2."""
    _problem_number = 2


class ProblemSolver(ABC):
    """Abstract class to find the solution for a single problem."""
    input_filepath = 'input.txt'

    def __init__(self):
        """Initialize the solver by loading any necessary data."""
        self._elves = self.load_elves()

    def load_elves(self) -> MultipleElves:
        """Load the elves from the filesystem into usable objects."""
        return ElfLoader(self.input_filepath).load_elves()


class ProblemOneSolver(ProblemSolver):
    """Class to find the solution for Problem #1."""
    def solve(self) -> ProblemOneSolution:
        """Find the number of calories carried by the elf with the most."""
        return ProblemOneSolution(
                self.get_elf_with_most_calories().get_total_calories())

    def get_elf_with_most_calories(self) -> Elf:
        """Find the single elf carrying the most calories."""
        return self.load_elves().get_elf_with_most_calories()


class ProblemTwoSolver(ProblemSolver):
    """Class to find the solution for Problem #2."""
    def solve(self) -> ProblemTwoSolution:
        """Find the number of calories carried by the 3 elves with the most."""
        return ProblemTwoSolution(
                self.get_n_elves_with_most_calories(3).get_total_calories())

    def get_n_elves_with_most_calories(self, num_elves: int) -> MultipleElves:
        """Find the n elves carrying the most calories."""
        return self._elves.get_n_elves_with_most_calories(num_elves)


class Chunk:
    """Class to represent on a chunk of the input file.

    A 'chunk' of the input file represents all the foods carried by a single
    elf. It is separated from all other chunks by a single blank line.
    """
    def __init__(self, chunk_string: str):
        """Initialize the chunk with a string from the filesystem.

        Args:
            chunk_string: A single newline-separated string, where each line
                represents a single food carried by a single elf.
        """
        self._chunk_string = chunk_string

    def to_elf(self) -> Elf:
        """Interpret the chunk as a single elf."""
        return Elf(list(self._to_foods()))

    def _to_foods(self) -> list[Food]:
        """Interpret the chunk as a series of Foods."""
        return [Food(calories) for calories in self._to_calories()]

    def _to_calories(self) -> list[Calories]:
        """Interpret the chunk as a series of Calories."""
        return [Calories(number) for number in self._to_numbers()]

    def _to_numbers(self) -> list[int]:
        """Interpret the chunk as a series of integers."""
        return [int(value) for value in self._to_strings()]

    def _to_strings(self) -> list[str]:
        """Interpret the chunk as a series of strings."""
        return list(string for string in self._chunk_string.split('\n'))

    def __repr__(self) -> str:
        """Print info about the chunk, for debugging purposes."""
        return f'Chunk<{self._chunk_string}>'


class FileReader:
    """Class to read a file from the local filesystem."""
    def __init__(self, filepath: str):
        """Initialize the file reader.

        Args:
            filepath: Path to the file on the local filesystem.
        """
        self._filepath = filepath

    def read_joined(self) -> str:
        """Read the file, joining newlines with no delimiter."""
        return ''.join(self.read_lines())

    def read_lines(self) -> list[str]:
        """Read the file, split on newlines."""
        return open(self._filepath).readlines()


class ChunkLoader:
    """Class to load Chunks from the input file."""
    def __init__(self, filepath):
        """Initialize the ChunkLoader with the input file.

        Args:
            filepath: The path to the input file on the local filesystem.
        """
        self._filepath = filepath

    def load_chunks(self) -> list[Chunk]:
        """Load all Chunks from the input file."""
        return [Chunk(chunk_str) for chunk_str in self.read_chunk_strings()]

    def read_chunk_strings(self) -> list[str]:
        """Read all chunk strings from the input file, to process into Chunks.

        For more about the expected contents of a chunk_string, see the
        docstring for Chunk.__init__.
        """
        return self.read_file().split('\n\n')

    def read_file(self) -> str:
        """Read the file from the filesystem, stripped and joined."""
        return self._file_reader().read_joined().strip()

    def _file_reader(self) -> FileReader:
        """Set up a FileReader to read the file."""
        return FileReader(self._filepath)


class ElfLoader:
    """Class to load elves from the filesystem into usable objects."""
    def __init__(self, filepath):
        """Initialize the ElfLoader with the local filepath.

        Args:
            filepath: Path to the input file on the local filesystem.
        """
        self._filepath = filepath

    def load_elves(self) -> MultipleElves:
        """Load all elves from the filesystem."""
        return MultipleElves([chunk.to_elf() for chunk in self._load_chunks()])

    def _load_chunks(self) -> list[Chunk]:
        """Load all Chunks from the local filesystem.."""
        return ChunkLoader(self._filepath).load_chunks()


def main():
    """Solve the two problems for Advent of Code, Day 1."""
    _ = [ps().solve().print() for ps in (ProblemOneSolver, ProblemTwoSolver)]


if __name__ == '__main__':
    main()
