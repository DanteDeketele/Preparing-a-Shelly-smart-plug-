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

### Prompt 5

> Searching for the MAC address of the Shelly smart plug... `AttributeError: module 'asyncio.subprocess' has no attribute 'run'`

### Changes made

- Replaced the incorrect `asyncio.subprocess` import in `shelly_setup.py` with Python's synchronous `subprocess` module.
- Corrected the Windows command from `network` to `networks`.

### Prompt 6

> The script found Shelly SSIDs, then failed with the old `asyncio.subprocess` error and printed the complete WLAN scan as the MAC address.

### Changes made

- Added `find_shelly_bssids()` to parse only Shelly SSIDs and their matching BSSID values.
- Changed the script to run one WLAN scan and print concise SSID-to-BSSID results.
- Removed the unused placeholder MAC address.
- Reverted that refactor at the user's request; the original script structure was preserved.