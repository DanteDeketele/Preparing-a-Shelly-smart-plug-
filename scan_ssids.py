"""Scan nearby Wi-Fi networks on Windows and return their SSIDs."""

from __future__ import annotations

import re
import subprocess


SSID_LINE = re.compile(r"^\s*SSID\s+\d+\s*:\s?(.*)$")
__all__ = ["scan_ssids"]


def scan_ssids() -> list[str]:
    """Return nearby non-empty SSIDs reported by the Windows WLAN service."""
    result = subprocess.run(
        ["netsh", "wlan", "show", "networks", "mode=bssid"],
        capture_output=True,
        text=True,
        check=True,
    )

    ssids: list[str] = []
    for line in result.stdout.splitlines():
        match = SSID_LINE.match(line)
        if match is not None and match.group(1) and match.group(1) not in ssids:
            ssids.append(match.group(1))
    return ssids


if __name__ == "__main__":
    print(scan_ssids())