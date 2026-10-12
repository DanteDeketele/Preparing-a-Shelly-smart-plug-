"""Connect to and disconnect from a Wi-Fi network on Windows."""

from __future__ import annotations

import re
import subprocess
import tempfile
import time
from xml.sax.saxutils import escape


TEMPORARY_PROFILES: set[str] = set()


class WifiConnectionError(RuntimeError):
    """Raised when Windows cannot connect to the requested SSID."""


def connected_ssid() -> str | None:
    """Return the SSID currently used by the active Wi-Fi connection."""
    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True,
        check=True,
    )
    match = re.search(r"^\s*SSID\s*:\s*(.+)$", result.stdout, re.MULTILINE)
    return match.group(1).strip() if match else None


def _add_profile(ssid: str, password: str | None = None) -> None:
    if password:
        security = f"""<authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{escape(password)}</keyMaterial>
            </sharedKey>"""
    else:
        security = """<authEncryption>
                <authentication>open</authentication>
                <encryption>none</encryption>
                <useOneX>false</useOneX>
            </authEncryption>"""

    profile = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{escape(ssid)}</name>
    <SSIDConfig>
        <SSID><name>{escape(ssid)}</name></SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>manual</connectionMode>
    <MSM>
        <security>
            {security}
        </security>
    </MSM>
</WLANProfile>"""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".xml", delete=False) as file:
        file.write(profile)
        profile_path = file.name

    try:
        result = subprocess.run(
            ["netsh", "wlan", "add", "profile", f"filename={profile_path}", "user=current"],
            capture_output=True,
            text=True,
            check=False,
        )
    finally:
        # The profile is stored by Windows; the temporary XML file is not needed.
        subprocess.run(["cmd", "/c", "del", "/q", profile_path], check=False)

    if result.returncode != 0:
        raise WifiConnectionError(result.stderr.strip() or result.stdout.strip())
    TEMPORARY_PROFILES.add(ssid)


def connect_to_ssid(ssid: str, password: str | None = None, timeout: float = 20) -> None:
    """Connect to an SSID, creating a temporary profile when needed."""
    if connected_ssid() == ssid:
        return

    result = subprocess.run(
        ["netsh", "wlan", "connect", f"name={ssid}", f"ssid={ssid}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        _add_profile(ssid, password)
        result = subprocess.run(
            ["netsh", "wlan", "connect", f"name={ssid}", f"ssid={ssid}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise WifiConnectionError(result.stderr.strip() or result.stdout.strip())

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if connected_ssid() == ssid:
            return
        time.sleep(1)

    raise WifiConnectionError(f"Timed out connecting to SSID {ssid!r}")


def disconnect_from_wifi() -> None:
    """Disconnect from the current Wi-Fi network without masking another error."""
    subprocess.run(
        ["netsh", "wlan", "disconnect"],
        capture_output=True,
        text=True,
        check=False,
    )
    for ssid in TEMPORARY_PROFILES:
        subprocess.run(
            ["netsh", "wlan", "delete", "profile", f"name={ssid}"],
            capture_output=True,
            text=True,
            check=False,
        )
    TEMPORARY_PROFILES.clear()