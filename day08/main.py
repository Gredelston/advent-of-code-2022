#!/usr/bin/env python3

import enum
from functools import cached_property
from typing import Optional


class Direction(enum.Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Tree:
    def __init__(self, height: int, row: int, col: int, grid: 'Grid'):
        self.height = height
        self.row = row
        self.col = col
        self.grid = grid
        self._cached_trees_to_edge: dict[Direction, list[Tree]] = {}

    def is_visible(self) -> bool:
        for direction in Direction:
            if self.is_visible_in_direction(direction):
                return True
        return False
    
    def is_visible_in_direction(self, direction: Direction) -> bool:
        trees_to_edge: list[Tree] = self.grid.find_trees_to_edge(self, direction)
        return all(other.height < self.height for other in trees_to_edge)

    def get_scenic_score(self) -> int:
        score = 1
        for direction in Direction:
            directional_score = self.get_scenic_score_in_direction(direction)
            score *= directional_score
        return score

    def get_scenic_score_in_direction(self, direction: Direction) -> int:
        score = 0
        trees_to_edge = self.find_trees_to_edge(direction)
        for tree in self.find_trees_to_edge(direction):
            score += 1
            if tree.height >= self.height:
                return score
        return score

    def find_trees_to_edge(self, direction: Direction) -> list['Tree']:
        if direction in self._cached_trees_to_edge:
            return self._cached_trees_to_edge[direction]
        trees_to_edge = self.grid.find_trees_to_edge(self, direction)
        self._cached_trees_to_edge[direction] = trees_to_edge
        return trees_to_edge

    def __str__(self):
        return str(self.height)

    def __repr__(self):
        return f'Tree<({self.row}, {self.col})->{self.height}>'


class Grid:
    def __init__(self, raw_file_contents: list[str]):
        trees_grid: list[list[Tree]] = []
        for row_num, row in enumerate(raw_file_contents):
            trees_row: list[Tree] = []
            for col_num, height in enumerate(row):
                trees_row.append(Tree(height, row_num, col_num, self))
            trees_grid.append(trees_row)
        self._grid = trees_grid

    @property
    def trees(self) -> list[Tree]:
        all_trees = []
        for row in self._grid:
            for tree in row:
                all_trees.append(tree)
        return all_trees

    def get_tree(self, row_num: int, col_num: int) -> Tree:
        return self._grid[row_num][col_num]
    
    @property
    def height(self) -> int:
        return len(self._grid)
    
    @property
    def width(self) -> int:
        return len(self._grid[0])

    def count_visible_trees(self) -> int:
        total = 0
        for tree in self.trees:
            if tree.is_visible():
                total += 1
        return total

    def find_trees_to_edge(self, from_tree: Tree, direction: Direction) -> list[Tree]:
        next_tree = self.find_next_tree_in_direction(from_tree, direction)
        if next_tree is None:
            return []
        else:
            return [next_tree] + self.find_trees_to_edge(next_tree, direction)

    def find_next_tree_in_direction(self, from_tree, direction) -> Optional[Tree]:
        if direction == Direction.UP:
            return self.find_next_tree_up(from_tree)
        elif direction == Direction.DOWN:
            return self.find_next_tree_down(from_tree)
        elif direction == Direction.LEFT:
            return self.find_next_tree_left(from_tree)
        elif direction == Direction.RIGHT:
            return self.find_next_tree_right(from_tree)
        raise ValueError(direction)

    def find_next_tree_up(self, from_tree: Tree) -> Optional[Tree]:
        if from_tree.row == 0:
            return None
        else:
            return self.get_tree(from_tree.row - 1, from_tree.col)

    def find_next_tree_down(self, from_tree: Tree) -> Optional[Tree]:
        if from_tree.row == self.height - 1:
            return None
        else:
            return self.get_tree(from_tree.row + 1, from_tree.col)

    def find_next_tree_left(self, from_tree: Tree) -> Optional[Tree]:
        if from_tree.col == 0:
            return None
        else:
            return self.get_tree(from_tree.row, from_tree.col - 1)

    def find_next_tree_right(self, from_tree: Tree) -> Optional[Tree]:
        if from_tree.col == self.width - 1:
            return None
        else:
            return self.get_tree(from_tree.row, from_tree.col + 1)
    
    def get_max_scenic_score(self) -> int:
        return max(tree.get_scenic_score() for tree in self.trees)

    def print(self):
        for row in self._grid:
            print(''.join(str(tree) for tree in row))


def main(use_sample: bool = False):
    """Solve part 1 of today's problem."""
    grid = load_grid(use_sample)
    print(f'\tPart 1: {grid.count_visible_trees()}')
    print(f'\tPart 2: {grid.get_max_scenic_score()}')


def part2(use_sample: bool = False) -> None:
    """Solve part 2 of today's problem."""
    grid = load_grid(use_sample)


def load_grid(use_sample: bool) -> Grid:
    """Load the input file to strings.

    Args:
        use_sample: Option to use the sample input instead of the real input.
    """
    fp = 'sample.txt' if use_sample else 'input.txt'
    with open(fp) as f:
        lines = f.readlines()
    return Grid([line.strip() for line in lines])


if __name__ == '__main__':
    print('Samples:')
    main(True)
    print('Real input:')
    main(False)
