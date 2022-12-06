#!/usr/bin/env python3

"""Solve Advent of Code 2022 Day 06."""


class Packet(str):
    """A short buffer of characters."""
    def are_all_chars_unique(self) -> bool:
        """Check whether all chars in this packet are unique."""
        return len(self) == len(set(self))


class Datastream(str):
    """The full datastream buffer, containing many characters."""
    def get_packet_at_position(self, position: int, length: int) -> Packet:
        """Extract the packet of {length} which ends at {position}."""
        assert position <= len(self)
        packet = Packet(self[max(position - length, 0) : position])
        assert len(packet) == min(position, length)
        return packet


def main(packet_length, use_sample: bool = False) -> int:
    """Find the first position marking a unique packet of a given length."""
    datastream = load_datastream(use_sample)
    for position in range(len(datastream)):
        packet = datastream.get_packet_at_position(position, packet_length)
        if len(packet) == packet_length and packet.are_all_chars_unique():
            return position
    raise ValueError('no start-of-packet marker found')


def load_datastream(use_sample: bool) -> Datastream:
    """Load the input file to strings.

    Args:
        use_sample: Option to use the sample input instead of the real input.
    """
    fp = 'sample.txt' if use_sample else 'input.txt'  # pylint: disable=invalid-name
    with open(fp) as f:  # pylint: disable=invalid-name
        lines = f.readlines()
    assert len(lines) == 1, len(lines)
    return Datastream(lines[0].strip())


if __name__ == '__main__':
    print('Samples:')
    print(f'\tPart 1: {main(4, True)}')
    print(f'\tPart 2: {main(14, True)}')
    print('Real input:')
    print(f'\tPart 1: {main(4, False)}')
    print(f'\tPart 2: {main(14, False)}')
