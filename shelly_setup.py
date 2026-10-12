import subprocess

from scan_ssids import scan_ssids

SSID_PREFIX = ["shellyplug-s"]
TAGET_MAC_ADDRESS = "00:1A:22:33:44:55"  # Replace with the actual MAC address of your Shelly smart plug

if __name__ == "__main__":
    ssids = scan_ssids()
    # check if any of the SSIDs start with the prefix
    shelly_ssids = [ssid for ssid in ssids if any(ssid.startswith(prefix) for prefix in SSID_PREFIX)]
    
    if not shelly_ssids:
        print("No Shelly smart plugs found.")
        exit(1)

    print("Shelly smart plugs found:")
    for ssid in shelly_ssids:
        print(f"- {ssid}")

    print("\nSearching for the MAC address of the Shelly smart plug...")
    for ssid in shelly_ssids:
        # search the mac address of the Shelly smart plug
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True,
            text=True,
            check=True,
        )

        mac_address = result.stdout.splitlines()
        print(f"MAC address for {ssid}: {mac_address}")
            