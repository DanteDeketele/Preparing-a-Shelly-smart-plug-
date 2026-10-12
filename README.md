# Shelly smart plug project

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