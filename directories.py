#!/usr/bin/env python3

from typing import Dict, Optional

_HELP = """Valid commands:
 - CREATE path/name
 - DELETE path/name
 - MOVE path1/name path2/name
 - LIST
 - HELP
"""

_DIRECTORY = {"/": {}}


def print_error(message):
    print(message)


def create(full_path: str) -> None:
    _dir = _DIRECTORY["/"]
    pieces = full_path.split("/")
    # TODO: Make sure that this is supposed to work like mkdir -p
    for path in pieces:
        if not path in _dir:
            _dir[path] = {}
        _dir = _dir[path]


def delete(full_path: str) -> None:
    _dir = _DIRECTORY["/"]
    pieces = full_path.split("/")
    last_path = pieces[-1]
    for path in pieces[:-1]:
        if not path in _dir:
            print_error(f"Cannot delete {full_path} - {path} does not exist")
            return
        _dir = _dir[path]

    if last_path in _dir:
        del _dir[last_path]


def move(full_path1: str, full_path2: str) -> None:
    pass


def _list_with_indent(obj: Optional[Dict], indent=0):
    if not obj:
        return
    for path, paths in obj.items():
        print(" " * indent + path)
        _list_with_indent(paths, indent + 1)


def list() -> None:
    _list_with_indent(_DIRECTORY["/"])


def help() -> None:
    print(_HELP)


_COMMANDS = {
    "create": create,
    "delete": delete,
    "move": move,
    "list": list,
    "help": help,
}


def main():
    print(_HELP)

    while True:
        full_command = input("")
        command = None
        args = []
        if not " " in full_command:
            command = full_command.lower()
        else:
            command, _, _args = full_command.partition(" ")
            command = command.lower()
            args = _args.split(" ")

        if not command in _COMMANDS:
            print_error("Invalid command")
            print_error(_HELP)
        else:
            try:
                _COMMANDS[command](*args)
            except TypeError as e:
                if "positional arguments but" in str(e):
                    print_error("Invalid arguments provided")
                    print_error(_HELP)
                else:
                    raise e


if __name__ == "__main__":
    main()
