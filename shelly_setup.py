from scan_ssids import scan_ssids

SSID_PREFIX = ["shellyplugs"]

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