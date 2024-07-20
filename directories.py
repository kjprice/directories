#!/usr/bin/env python3

from typing import Dict, Optional

_HELP = """Valid commands:
 - CREATE path/name
 - DELETE path/name
 - MOVE path1/name path2/name
 - LIST
 - HELP
"""


def print_error(message):
    print(message)


def help() -> None:
    print(_HELP)


class Directory:
    def __init__(self) -> None:
        self.directory = None
        self.reset()

    def reset(self):
        """Helper for testing"""
        self.directory = {"/": {}}

    @property
    def root(self):
        """Simply returns the root directory (children of "/")"""
        return self.directory["/"]

    def create(self, full_path: str) -> None:
        """Mutates self.directory. Works same as `mkdir -p`: deeply creates paths if they do not exist"""
        _dir = self.root
        pieces = full_path.split("/")
        # TODO: Make sure that this is supposed to work like mkdir -p
        for path in pieces:
            if not path in _dir:
                _dir[path] = {}
            _dir = _dir[path]

    def delete(self, full_path: str) -> None:
        """Mutates self.directory. Deletes deepest directory if exists."""
        _dir = self.root
        pieces = full_path.split("/")
        last_path = pieces[-1]
        for path in pieces[:-1]:
            if not path in _dir:
                print_error(f"Cannot delete {full_path} - {path} does not exist")
                return
            _dir = _dir[path]

        if last_path in _dir:
            del _dir[last_path]

    def _get(self, full_path: str) -> Optional[Dict]:
        """Helper function to retrieve directory object from nested paths"""
        _dir = self.root
        for path in full_path.split("/"):
            if not path in _dir:
                return None
            _dir = _dir[path]
        return _dir

    def move(self, full_path1: str, full_path2: str) -> None:
        """Mutates self.directory. Adds the last path (and descendents) from full_path1 to the end of full_path2.
        Will overwrite Data. Deletes the last path from full_path1."""
        pieces1 = full_path1.split("/")
        last_path1 = pieces1[-1]
        paths_from = self._get(full_path1)
        if paths_from is None:
            print_error(f"Cannot move {full_path1} - subpath does not exist")
            return

        self.create(full_path2)
        path_to = self._get(full_path2)

        path_to[last_path1] = paths_from
        self.delete(full_path1)

    def _list_with_indent(self, obj: Optional[Dict], indent=0):
        """Helper. Allows to recursively print with indententaion"""
        if not obj:
            return
        keys = sorted(obj.keys())

        for path in keys:
            paths = obj[path]
            print("  " * indent + path)
            self._list_with_indent(paths, indent + 1)

    def list(self) -> None:
        self._list_with_indent(self.root)


directory = Directory()


_COMMANDS = {
    "create": directory.create,
    "delete": directory.delete,
    "move": directory.move,
    "list": directory.list,
    "help": help,
}


def run_full_command(full_command: str):
    """Takes any valid command (eg. "create vegetables") and runs the corresponding function"""
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
    """Main method - continuously listens for user input, runs provided command"""
    print(_HELP)

    while True:
        full_command = input("")
        run_full_command(full_command)


if __name__ == "__main__":
    main()
