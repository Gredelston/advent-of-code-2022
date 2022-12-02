#!/usr/bin/env python3

import enum
import typing


USE_SAMPLE = True


class Shape(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(enum.Enum):
    LOSS = 1
    DRAW = 2
    WIN = 3


YOUR_SHAPE_SYMBOLS: dict[str, Shape] = {
        'A': Shape.ROCK,
        'B': Shape.PAPER,
        'C': Shape.SCISSORS,
}
MY_SHAPE_SYMBOLS: dict[str, Shape] = {
        'X': Shape.ROCK,
        'Y': Shape.PAPER,
        'Z': Shape.SCISSORS,
}
DESIRED_OUTCOME_SYMBOLS: dict[str, Outcome] = {
        'X': Outcome.LOSS,
        'Y': Outcome.DRAW,
        'Z': Outcome.WIN,
}
Score = typing.NewType('Score', int)


class RPSRound:
    def __init__(self, my_shape: Shape, your_shape: Shape):
        self._my_shape = my_shape
        self._your_shape = your_shape

    def get_round_score(self) -> Score:
        return Score(self.get_shape_score() + self.get_outcome_score())
    
    def get_shape_score(self) -> Score:
        SHAPE_SCORES: dict[Shape, Score] = {
                Shape.ROCK: Score(1),
                Shape.PAPER: Score(2),
                Shape.SCISSORS: Score(3),
        }
        return SHAPE_SCORES[self._my_shape]

    def get_outcome_score(self) -> Score:
        OUTCOME_SCORES: dict[Outcome, Score] = {
                Outcome.LOSS: Score(0),
                Outcome.DRAW: Score(3),
                Outcome.WIN: Score(6),
        }
        return OUTCOME_SCORES[self.get_outcome()]

    def get_outcome(self) -> Outcome:
        OUTCOME_MAP: dict[tuple[Shape, Shape], Outcome] = {
                (Shape.ROCK, Shape.ROCK): Outcome.DRAW,
                (Shape.ROCK, Shape.PAPER): Outcome.LOSS,
                (Shape.ROCK, Shape.SCISSORS): Outcome.WIN,

                (Shape.PAPER, Shape.ROCK): Outcome.WIN,
                (Shape.PAPER, Shape.PAPER): Outcome.DRAW,
                (Shape.PAPER, Shape.SCISSORS): Outcome.LOSS,

                (Shape.SCISSORS, Shape.ROCK): Outcome.LOSS,
                (Shape.SCISSORS, Shape.PAPER): Outcome.WIN,
                (Shape.SCISSORS, Shape.SCISSORS): Outcome.DRAW,
        }
        return OUTCOME_MAP[(self._my_shape, self._your_shape)]

    def __repr__(self) -> str:
        return f'RPSRound<{self._my_shape}, {self._your_shape} -> {self.get_round_score()}>'



def part1():
    file_contents = load_file()
    rps_rounds = interpret_file_contents_part_1(file_contents)
    total_score = get_total_score(rps_rounds)
    print(total_score)


def load_file() -> list[str]:
    fp = 'sample.txt' if USE_SAMPLE else 'input.txt'
    lines = open(fp).readlines()
    return [line.strip() for line in lines]


def interpret_file_contents_part_1(file_contents: list[str]) -> list[RPSRound]:
    rps_rounds = []
    for line in file_contents:
        your_symbol, my_symbol = line.split()
        your_shape = YOUR_SHAPE_SYMBOLS[your_symbol]
        my_shape = MY_SHAPE_SYMBOLS[my_symbol]
        rps_rounds.append(RPSRound(my_shape, your_shape))
    return rps_rounds


def get_total_score(rps_rounds: list[RPSRound]) -> Score:
    score = Score(0)
    for rps_round in rps_rounds:
        score += rps_round.get_round_score()
    return score


def part2():
    file_contents = load_file()
    rps_rounds = interpret_file_contents_part_2(file_contents)
    total_score = get_total_score(rps_rounds)
    print(total_score)


def interpret_file_contents_part_2(file_contents: list[str]) -> list[RPSRound]:
    rps_rounds = []
    for line in file_contents:
        your_symbol, desired_outcome_symbol = line.split()
        your_shape = YOUR_SHAPE_SYMBOLS[your_symbol]
        desired_outcome = DESIRED_OUTCOME_SYMBOLS[desired_outcome_symbol]
        my_shape = determine_my_shape(your_shape, desired_outcome)
        rps_rounds.append(RPSRound(my_shape, your_shape))
    return rps_rounds


def determine_my_shape(your_shape: Shape, desired_outcome: Outcome) -> Shape:
    for test_shape in Shape:
        test_rps_round = RPSRound(test_shape, your_shape)
        if test_rps_round.get_outcome() == desired_outcome:
            return test_shape
    raise Exception(
            'Didn\'t find valid shape for ({your_shape}, {desired_outcome})')


if __name__ == '__main__':
    part1()
    part2()
