# Shelly smart plug project

USE the shelly_setup.py

## Environment setup

Create or refresh the local virtual environment with:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the starter program with:

```powershell
python hello_world.py
```

Scan for nearby Wi-Fi SSIDs on Windows with:

```powershell
python scan_ssids.py
```

Use the scanner from another Python script with:

```python
from scan_ssids import scan_ssids

nearby_ssids = scan_ssids()
print(nearby_ssids)
```

Send a Gen1 Shelly request with form parameters from another script with:

```python
from shelly_api import send_request

# The SSID is the Wi-Fi name, not an IP address.
# A factory-reset Gen1 Shelly uses 192.168.33.1 in setup mode.
response = send_request(
	"http://192.168.33.1/settings/relay/0",
	{"name": "deketele-dante-Outlet1"},
)
print(response)
```

Run the configuration script with the required outlet name:

```powershell
python shelly_setup.py --name "deketele-dante-Outlet1"
```

Cloud is disabled by default. Enable it explicitly with `--cloud` or disable it with `--no-cloud`.

The setup disables both the power LED and the Wi-Fi status LED.

The Wi-Fi helpers connect by SSID and always disconnect afterward:

```python
from wifi_connection import connect_to_ssid, disconnect_from_wifi

connect_to_ssid("shellyplug-s-7C87CEB55241")
try:
	# Send requests to http://192.168.33.1 while connected.
	pass
finally:
	disconnect_from_wifi()
```