# filerazor

An interactive terminal utility for reviewing and deleting files in a directory, one by one. Supports tab-completion on path input, real-time file preview, alphabetical traversal, and an optional folder deletion mode.

## Platform Support

Linux and macOS only. Windows is not supported due to the following incompatibilities:

- `readline` is a Unix library and is not available on Windows by default
- `readchar` behaves differently on Windows and may not work as expected
- `os.system('clear')` is Unix only
- ANSI escape codes used for the status display may not render correctly in older Windows terminals
- Path handling assumes Unix-style paths

## Dependencies

Install required packages with pip:

    pip install colorama readchar

## Usage

Run the script:

    python filerazor.py

You will first be prompted to enter a directory path. Tab completion is supported.

    Enter path: /home/user/Downloads/

You will then be asked whether to include folders in the deletion process:

    Would you like to delete folders? y/n:

Once confirmed, filerazor will walk through each file in the directory alphabetically, prompting you for an action on each one.

## Options

    y    Delete the current file permanently.
    n    Skip the current file and move to the next.
    o    Open and preview the contents of the current file, then re-prompt.

## Display

The name of the current file being reviewed is shown in the top right corner of the terminal at all times. The result of the last action (deleted, skipped, or file contents) is shown just below it, so you always have context on what was last done.

## Notes

- Deletion is permanent. There is no trash or undo.
- Binary files opened with `o` will display with unrecognized characters replaced.
- If folder deletion is disabled, directories are silently skipped.
- Any input other than y, n, or o will re-prompt for the same file.
