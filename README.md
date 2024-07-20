# Directories

This is a basic utility that enables interaction with a mock file system.

Note that the filesystem is not persisted. Allowing this feature would be trivial if we were to store the Directory.directory object in a json file. This feature can be added if requested.

The script should be ran by executing the directories.py file and can be tested (including the requirements provided) by running the commands below.

If I were to spend more time on this, I would change the following:

1. Further decouple the code so that the Directory class lives in its own file
2. Implement a persistent state (such as sql lite or just a json file)
3. Allow for command line arguments (ie "argparse") so that commands can be ran via "./directories.py create fruit". Currently you must execute the script and provide commands using the prompt provided

## Run Script

./directories.py

Simply follow the prompt instructions. Provide commands such as "CREATE fruit" and "List". Note that the commands are not case sensitive ("LIST" and "list" both work).

## Run Tests

python3 -m unittest discover

## Troubleshooting

If an error occurs when running the script, there may be an issue with your environment variables. If this is the case, try running using `path/to/your/python3/interpreter directories.py`.

Also, be sure you are in the project's root directory before running any commands.
