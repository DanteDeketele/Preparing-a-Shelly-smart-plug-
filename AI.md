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

### Prompt 7

> My script returns too much info, not just the MAC.

### Changes made

- Updated only the output parsing in `shelly_setup.py`.
- The script now selects the matching Shelly SSID block and prints only its first BSSID/MAC address.
- Corrected the delimiter handling so the complete six-octet MAC address is retained.

### Prompt 8

> clean up the script a bit, dont change the actual code or logic, you can move things into definitions or seperate files

### Changes made

- Split `.env` loading, Shelly SSID filtering, target SSID lookup, and orchestration into functions in `shelly_setup.py`.
- Preserved the existing commands, comparisons, constants, output messages, and exit behavior.

### Prompt 9

> make a file to send api requests to the shelly that take in a url and body

### Changes made

- Added `shelly_api.py` with an importable `send_request(url, body)` function.
- The helper sends JSON using an HTTP POST and returns the decoded JSON response.
- Added clear errors for failed requests and non-object JSON responses.
- Documented an example request in `README.md`.

### Prompt 10

> nah this isnt right you cant use an assid as an ip adress right?

### Changes made

- Clarified in `README.md` that an SSID is a Wi-Fi name, not an IP address.
- Documented that `192.168.33.1` is the factory-reset Shelly setup IP used in the API example.

### Prompt 11

> fix the script, maybe you need to add connect and disconnect definitions based on an SSID, and make sure it does not break if I reboot the device using the script

### Changes made

- Added `wifi_connection.py` with `connect_to_ssid()` and `disconnect_from_wifi()`.
- Connected to the selected Shelly SSID before the API request and disconnected in `finally` so cleanup still runs after request or reboot errors.
- Changed the API request URL to use `http://192.168.33.1` instead of a path-only URL.
- Documented the connection lifecycle in `README.md`.
- Added `reboot_device()` to `shelly_api.py` for a delayed reboot request.

### Prompt 14

> `## /settings/relay/0` Think this is the actual url

### Changes made

- Confirmed the device is a Gen1 Shelly Plug S based on its `shellyplug-s-...` SSID.
- Changed the setup endpoint to `/settings/relay/0`.
- Changed API request bodies from JSON to Gen1 `application/x-www-form-urlencoded` parameters.
- Changed the reboot endpoint from Gen2 RPC to Gen1 `/reboot`.

### Prompt 15

> Add `default_state` off after restart, disable `led_power_disable`, enable MQTT, set `max_power` to 2200 W, set the Wi-Fi, and disable all unused services.

### Changes made

- Configured relay name, `default_state=off`, and `max_power=2200` through `/settings/relay/0`.
- Disabled the Plug S power LED with `led_power_disable=1`.
- Enabled MQTT with broker `172.23.83.254:1883` and the configured name as `mqtt_id`.
- Disabled cloud, CoIoT, SNTP, debug logging, discovery, and Wi-Fi recovery reboot.
- Configured STA Wi-Fi for `Howest-IoT` using the password from `.env`.
- Sent the Wi-Fi configuration last because the Shelly leaves its setup AP after applying it.

### Prompt 16

> The Wi-Fi SSID is also in `.env`, and the assignment asks to have script parameters.

### Changes made

- The setup script now reads both `WIFI_SSID` and `WIFI_PASSWORD` from `.env`.
- Added required `--name` command-line parameter for the outlet name.
- Added optional `--cloud` / `--no-cloud` parameter, defaulting to cloud disabled.

### Prompt 17

> add a bit more prints

### Changes made

- Added progress messages for credential loading, device discovery, Wi-Fi connection, each configuration stage, cloud state, Wi-Fi handoff, and cleanup.
- No passwords or other secrets are printed.

### Prompt 18

> also check if it connected successfuly to mqtt and wifi

### Changes made

- Added password-protected Wi-Fi profile support to `wifi_connection.py`.
- After configuring STA mode, the script reconnects to the configured Wi-Fi network.
- It resolves the Shelly `.local` hostname, reads `/status`, and prints the actual Wi-Fi and MQTT connection states.

### Prompt 19

> Verification failed with `[Errno 11001] getaddrinfo failed` after reconnecting to `Howest-IoT`.

### Changes made

- Added a Windows ARP-table fallback when Shelly mDNS hostname resolution is unavailable.
- The fallback matches the Shelly MAC suffix and uses the discovered DHCP IP for `/status` verification.

### Prompt 20

> maybe arp -a was executed too fast

### Changes made

- Changed ARP discovery to retry for up to 15 seconds, allowing Windows time to populate the Shelly entry after reconnecting to Wi-Fi.

### Prompt 23

> The Shelly still cannot be found after the ARP retries; use Nmap.

### Changes made

- Added Nmap discovery fallback for `172.30.248.0/21`.
- Nmap matches the Shelly MAC suffix and is used only after mDNS and ARP discovery fail.
- The script now reports a specific discovery failure instead of re-raising an unrelated DNS error.

### Prompt 21

> maybe reboot the device first?

### Changes made

- Added a Gen1 `/reboot` call after MQTT, service, and cloud settings.
- Reconnects to the Shelly setup SSID after reboot before applying the final STA Wi-Fi configuration.

### Prompt 22

> The Gen1 implementation still does not work: the Shelly is not visible on Wi-Fi or the MQTT broker.

### Changes made

- Corrected Gen1 Cloud/MQTT ordering: Cloud is configured first, and MQTT is configured last because Gen1 automatically disables Cloud when MQTT is enabled.
- Added a warning when `--cloud` is used because MQTT takes priority on Gen1.
- Removed the Wi-Fi password from progress output.

### Prompt 12

> `WifiConnectionError: There is no profile "shellyplug-s-7C87CEB55241" assigned to the specified interface.`

### Changes made

- Updated `wifi_connection.py` to create a temporary Windows open-network profile when the Shelly SSID has no saved profile.
- The temporary profile is removed during `disconnect_from_wifi()`.

### Prompt 13

> `WinError 10051: An attempt was made to perform a socket operation on an unreachable network` after connecting to the Shelly SSID.

### Changes made

- Added bounded retries to `send_request()` for the short period while Windows finishes assigning the Wi-Fi route/IP.
- The same retry behavior also tolerates a brief network interruption caused by a Shelly reboot.