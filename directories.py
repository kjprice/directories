#!/usr/bin/env python3

from typing import Dict, Optional

_HELP = """Valid commands:
 - CREATE path/name
 - DELETE path/name
 - MOVE path1/name path2/name
 - LIST
 - HELP
"""

_DIRECTORY = None


def reset():
    global _DIRECTORY
    _DIRECTORY = {"/": {}}


def get_root():
    return _DIRECTORY["/"]


reset()


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


def get(full_path: str) -> Optional[Dict]:
    _dir = _DIRECTORY["/"]
    for path in full_path.split("/"):
        if not path in _dir:
            return None
        _dir = _dir[path]
    return _dir


""" TODO: Test:
full_path1 does not exist
full_path2 already exists
full_path2 does not exist (subpath)
full_path2 does not exist (full path)

Make sure that last dir in full_path1 is deleted
Make sure that new dir exists in full_path2

TODO: This is broken:
create 1/2/3/4
move 1/2 2/3
"""


def move(full_path1: str, full_path2: str) -> None:
    paths_from = get(full_path1)
    if paths_from is None:
        print_error(f"Cannot move {full_path1} - subpath does not exist")
        return

    if get(full_path2) is not None:
        print_error(
            f"Cannot move {full_path1} - the path {full_path2} exists and would be overridden"
        )
        return

    pieces2 = full_path2.split("/")
    last_path2 = pieces2[-1]
    path_to = get("/".join(pieces2[:-1]))
    if path_to is None:
        create(full_path2)
        path_to = get("/".join(pieces2[:-1]))

    path_to[last_path2] = paths_from
    delete(full_path1)


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


def run_full_command(full_command: str):
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


def main():
    print(_HELP)

    while True:
        full_command = input("")
        run_full_command(full_command)


if __name__ == "__main__":
    main()
