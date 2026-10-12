# AI change log

This file records AI-assisted prompts and the changes made to the repository.

## 2026-10-12

### Prompt 1

> For all AI tasks, maje a ai doc to know wich chnages and propts where made. make a python script base for the repo

### Prompt 2

> nope, I didnt ask you to make the assignment, make a hellow world, im doing the coding, make the envirement

### Changes made

- Added `hello_world.py` as a minimal Python entry point.
- Created the local `.venv` Python virtual environment.
- Added `.vscode/settings.json` to select `.venv` in VS Code.
- Added `.gitignore` for the virtual environment and Python cache files.
- Added `requirements.txt` as the dependency placeholder.
- Added `README.md` with setup and run commands.
- Did not implement the Shelly assignment; that coding remains for the student.

### Prompt 3

> get a list of strings of ssids in the air

### Changes made

- Added `scan_ssids.py` with `scan_ssids() -> list[str]`.
- The scanner uses Windows `netsh`, removes empty entries and duplicates, and prints the SSID list when run directly.
- Added the scanner command to `README.md`.

### Verification

- Confirmed Windows exposes an active Wi-Fi interface named `Wi-Fi`.

### Prompt 4

> make the scan ssid a usable definition for my own script

### Changes made

- Marked `scan_ssids` as the public importable definition in `scan_ssids.py`.
- Added an import-and-call example to `README.md`.