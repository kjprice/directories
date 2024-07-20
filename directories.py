#!/usr/bin/env python3

_HELP = """Valid commands:
 - CREATE path/name
 - DELETE path/name
 - MOVE path1/name path2/name
 - LIST
 - HELP
"""

_DIRECTORY = {"/": {}}


def create(path: str) -> None:
    pass


def delete(path: str) -> None:
    pass


def move(path1: str, path2: str) -> None:
    pass


def list() -> None:
    pass


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
            print("Invalid command")
            print(_HELP)
        else:
            try:
                _COMMANDS[command](*args)
            except TypeError as e:
                if "positional arguments but" in str(e):
                    print("Invalid arguments provided")
                    print(_HELP)
                else:
                    raise e


if __name__ == "__main__":
    main()
