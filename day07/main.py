#!/usr/bin/env python3

from abc import ABC
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Optional


class FilesystemEntityType(Enum):
    UNSPECIFIED = 0
    FILE = 1
    DIRECTORY = 2


class FilesystemEntity(ABC):
    entity_type = FilesystemEntityType.UNSPECIFIED

    def __init__(self, name: str, parent: Optional['Directory']):
        self.name = name
        self.parent = parent

    @property
    def entity_type(self) -> FilesystemEntityType:
        return FilesystemEntityType.UNSPECIFIED

    def abspath(self) -> Path:
        if self.parent is None:
            return Path(self.name)
        else:
            return self.parent.abspath / self.name

    @property
    def is_file(self) -> bool:
        return self.entity_type == FilesystemEntityType.FILE

    @property
    def is_dir(self) -> bool:
        return self.entity_type == FilesystemEntityType.DIRECTORY


class File(FilesystemEntity):
    entity_type = FilesystemEntityType.FILE

    def __init__(self, name: str, parent: 'Directory', size: int):
        self.name = name
        self.size = size

    def __repr__(self) -> str:
        return f'File<{self.name}, {self.size}>'


class Directory(FilesystemEntity):
    entity_type = FilesystemEntityType.DIRECTORY

    def __init__(self, name: str, parent: Optional['Directory'] = None,
                 child_names: Optional[list[str]] = None):
        self.name = name
        self.child_names: list[str] = []
        if child_names is not None:
            self.child_names: list[str] = child_names

    def __repr__(self) -> str:
        return f'Directory<{self.name}>'


class FilesystemMap(dict[Path, FilesystemEntity]):
    def get_entity_size(self, entity_path: Path) -> int:
        entity = self[entity_path]
        if entity.is_file:
            return entity.size
        else:
            total_size = 0
            for child_name in entity.child_names:
                child_path = entity_path / child_name
                child_entity = self[child_path]
                total_size += self.get_entity_size(child_path)
            return total_size


class Command(ABC):
    is_cd = False
    is_ls = False


class LsCommand(Command):
    is_ls = True

    def __init__(self, response: list[str]):
        self._response = response

    def files(self, called_from: Directory) -> list[File]:
        files: list[File] = []
        for line in self._response:
            if line.split()[0] == 'dir':
                continue
            size = int(line.split()[0])
            name = line.split()[1]
            files.append(File(name, called_from, size))
        return files

    def child_dir_names(self) -> list[str]:
        dir_names: list[str] = []
        for line in self._response:
            if line.split()[0] != 'dir':
                continue
            dir_names.append(line.split()[1])
        return dir_names

    @property
    def child_names(self) -> list[str]:
        return [line.split()[1] for line in self._response]

    def __repr__(self) -> str:
        return f'$ ls'


class CdCommand(Command):
    is_cd = True

    def __init__(self, arg: str):
        self.arg = arg

    def __repr__(self) -> str:
        return f'$ cd {self.arg}'


def load_file_contents(use_sample: bool) -> list[str]:
    """Load the input file to strings.

    Args:
        use_sample: Option to use the sample input instead of the real input.
    """
    fp = 'sample.txt' if use_sample else 'input.txt'
    with open(fp) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def create_commands(file_contents: list[str]) -> list[Command]:
    command_chunks: list[str] = '\n'.join(file_contents).split('$')
    commands: list[Command] = []
    for command_chunk in command_chunks:
        command_chunk = command_chunk.strip()
        if not command_chunk:
            continue
        lines = command_chunk.split('\n')
        cmd_line = lines[0]
        response_lines = lines[1:]
        if cmd_line.split()[0] == 'cd':
            assert len(response_lines) == 0, command_chunk
            commands.append(CdCommand(cmd_line.split()[1]))
        elif cmd_line.split()[0] == 'ls':
            assert len(cmd_line.split()) == 1, cmd_line
            commands.append(LsCommand(response_lines))
    return commands


def crawl_filesystem(commands: list[Command]) -> FilesystemMap:
    """Run the commands to build a model of the filesystem."""
    cwd = Path('/') # Current working directory
    fs_map = FilesystemMap({cwd: Directory('/')})
    for command in commands:
        if command.is_cd:
            cwd = (cwd / command.arg).resolve()
        elif command.is_ls:
            this_dir = fs_map[cwd]
            this_dir.child_names = command.child_names
            for child_file in command.files(cwd):
                path = cwd / child_file.name
                fs_map[path] = child_file
            for child_dir_name in command.child_dir_names():
                path = cwd / child_dir_name
                fs_map[path] = Directory(child_dir_name, this_dir)
        else:
            raise ValueError(f'Unexpected command: {command}')
    return fs_map


def sum_small_dirs(fs_map: FilesystemMap) -> int:
    MAX_SIZE = 100000
    valid_dirs: list[Directory] = []
    for entity_path, entity in fs_map.items():
        if not entity.is_dir:
            continue
        size = fs_map.get_entity_size(entity_path)
        if size > MAX_SIZE:
            continue
        valid_dirs.append(entity_path)
    return sum(fs_map.get_entity_size(directory_path) for directory_path in valid_dirs)


def part1(use_sample: bool = False) -> int:
    """Solve part 1 of today's problem."""
    file_contents: list[str] = load_file_contents(use_sample)
    commands: list[Command] = create_commands(file_contents)
    fs_map = crawl_filesystem(commands)
    return sum_small_dirs(fs_map)


def find_deleteable_paths(fs_map: FilesystemMap) -> list[Path]:
    TOTAL_DISK_SPACE = 70000000
    REQUIRED_UNUSED_SPACE = 30000000
    current_used_space = fs_map.get_entity_size(Path('/'))
    current_unused = TOTAL_DISK_SPACE - current_used_space
    space_to_free = REQUIRED_UNUSED_SPACE - current_unused
    deleteable_paths: list[Directory] = []
    for entity_path, entity in fs_map.items():
        if not entity.is_dir:
            continue
        if fs_map.get_entity_size(entity_path) > space_to_free:
            deleteable_paths.append(entity_path)
    return deleteable_paths


def part2(use_sample: bool = False) -> None:
    """Solve part 2 of today's problem."""
    file_contents = load_file_contents(use_sample)
    commands = create_commands(file_contents)
    fs_map = crawl_filesystem(commands)
    deleteable_paths = find_deleteable_paths(fs_map)
    return min(fs_map.get_entity_size(path) for path in find_deleteable_paths(fs_map))



if __name__ == '__main__':
    print('Samples:')
    print(f'\tPart 1: {part1(True)}')
    print(f'\tPart 2: {part2(True)}')
    print('Real input:')
    print(f'\tPart 1: {part1(False)}')
    print(f'\tPart 2: {part2(False)}')
