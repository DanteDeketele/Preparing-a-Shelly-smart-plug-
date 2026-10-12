import subprocess
import argparse
import socket
import time
from shelly_api import reboot_device, send_request, ShellyApiError

from scan_ssids import scan_ssids
from wifi_connection import WifiConnectionError, connect_to_ssid, disconnect_from_wifi

SSID_PREFIX = ["shellyplug-s"]
TARGET_MAC_ADDRESS = "7e:87:ce:b5:52:41"  # Replace with the actual MAC address of your Shelly smart plug

SHELLY_IP = "192.168.33.1"
MQTT_SERVER = "172.23.83.254:1883"
MAX_POWER_WATTS = 2200
IOT_NETWORK = "172.30.248.0/21"

def load_wifi_credentials() -> tuple[str | None, str | None]:
    ssid = None
    password = None
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("WIFI_SSID="):
                ssid = line.strip().split("=")[1]
            elif line.startswith("WIFI_PASSWORD="):
                password = line.strip().split("=")[1]
    return ssid, password


def find_shelly_ssids() -> list[str]:
    ssids = scan_ssids()
    return [ssid for ssid in ssids if any(ssid.startswith(prefix) for prefix in SSID_PREFIX)]


def find_target_ssid(shelly_ssids: list[str]) -> str | None:
    print("\nSearching for the MAC address of the Shelly smart plug...")
    for ssid in shelly_ssids:
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True,
            text=True,
            check=True,
        )

        mac_address = None
        matching_ssid = False
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("SSID "):
                matching_ssid = line.split(":", 1)[-1].strip() == ssid
            elif matching_ssid and line.startswith("BSSID "):
                mac_address = line.split(":", 1)[-1].strip()
                break

        if mac_address == TARGET_MAC_ADDRESS:
            print(f"Found target Shelly smart plug with MAC address {TARGET_MAC_ADDRESS} and SSID {ssid}.")
            return ssid
    return None


def find_device_ip_from_arp(mac_address: str, timeout: float = 15) -> str | None:
    mac_suffix = mac_address.lower().replace(":", "").replace("-", "")[2:]
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = subprocess.run(
            ["arp", "-a"],
            capture_output=True,
            text=True,
            check=False,
        )
        for line in result.stdout.splitlines():
            fields = line.split()
            if len(fields) >= 2:
                arp_mac = fields[1].lower().replace("-", "")
                if arp_mac[2:] == mac_suffix:
                    return fields[0].strip("()")
        print("Shelly IP is not in the ARP cache yet; waiting...")
        time.sleep(1)
    return None


def find_device_ip_with_nmap(mac_address: str) -> str | None:
    print(f"Scanning {IOT_NETWORK} with Nmap...")
    try:
        result = subprocess.run(
            ["nmap", "-sn", "-PR", "-n", IOT_NETWORK, "-oG", "-"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        print("Nmap is not installed; skipping Nmap discovery.")
        return None

    mac_suffix = mac_address.lower().replace(":", "").replace("-", "")[2:]
    current_ip = None
    for line in result.stdout.splitlines():
        if line.startswith("Host:") and "Status: Up" in line:
            current_ip = line.split()[1]
        elif current_ip and "MAC Address:" in line:
            nmap_mac = line.split("MAC Address:", 1)[1].split()[0].lower().replace(":", "")
            if nmap_mac[2:] == mac_suffix:
                return current_ip
    return None


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configure a factory-reset Shelly Plug S.")
    parser.add_argument("--name", required=True, help="Relay name, for example Doe-Jane-Outlet1")
    parser.add_argument(
        "--cloud",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable Shelly Cloud (disabled by default)",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    print(f"Starting Shelly setup for '{arguments.name}'.")
    wifi_ssid, wifi_password = load_wifi_credentials()
    if not wifi_ssid or not wifi_password:
        print("WIFI_SSID and WIFI_PASSWORD are required in .env.")
        exit(1)
    print(f"Loaded Wi-Fi settings for SSID '{wifi_ssid}'.")

    shelly_ssids = find_shelly_ssids()
    print(f"Found {len(shelly_ssids)} Shelly SSID(s) nearby.")

    if not shelly_ssids:
        print("No Shelly smart plugs found.")
        exit(1)

    target_ssid = find_target_ssid(shelly_ssids)

    if not target_ssid:
        print(f"No Shelly smart plug found with MAC address {TARGET_MAC_ADDRESS}.")
        print("Please ensure the Shelly smart plug is powered on and in pairing mode.")
        print("Check the script if the MAC address is correct and matches the one on your Shelly smart plug.")
        exit(1)

    print(f"Connecting to Shelly SSID '{target_ssid}'.")
    connect_to_ssid(target_ssid)
    print(f"Connected to '{target_ssid}'.")

    base_url = f"http://{SHELLY_IP}"

    try:
        print("Configuring relay name, startup state, and maximum power...")
        send_request(
            f"{base_url}/settings/relay/0",
            {
                "name": arguments.name,
                "default_state": "off",
                "max_power": MAX_POWER_WATTS,
            },
        )
        if arguments.cloud:
            print("Warning: Gen1 MQTT disables Shelly Cloud; MQTT will take priority.")
        print(f"Setting Shelly Cloud to {'enabled' if arguments.cloud else 'disabled'}...")
        send_request(f"{base_url}/settings/cloud", {"enabled": int(arguments.cloud)})
        print("Configuring LEDs, MQTT, and unused services...")
        send_request(
            f"{base_url}/settings",
            {
                "name": arguments.name,
                "led_power_disable": 1,
                "mqtt_enable": 1,
                "mqtt_server": MQTT_SERVER,
                "mqtt_id": arguments.name,
                "coiot_enable": 0,
                "sntp_server": "",
                "debug_enable": 0,
                "discoverable": 0,
                "wifirecovery_reboot_enabled": 0,
            },
        )
        print("Rebooting Shelly to apply MQTT and service settings...")
        reboot_device(base_url)
        disconnect_from_wifi()
        time.sleep(5)
        print(f"Reconnecting to Shelly SSID '{target_ssid}' after reboot...")
        connect_to_ssid(target_ssid)
        print(f"Configuring Wi-Fi client mode for '{wifi_ssid}'...")
        send_request(
            f"{base_url}/settings/sta",
            {
                "enabled": 1,
                "ssid": wifi_ssid,
                "key": wifi_password,
                "ipv4_method": "dhcp",
            },
        )
        print("Reconnecting to the configured Wi-Fi to verify device status...")
        disconnect_from_wifi()
        connect_to_ssid(wifi_ssid, wifi_password)
        device_host = f"{target_ssid}.local"
        try:
            device_ip = socket.gethostbyname(device_host)
            print(f"Resolved Shelly hostname '{device_host}' to {device_ip}.")
        except socket.gaierror:
            print("mDNS lookup failed; waiting for the Shelly IP in the ARP table...")
            device_ip = find_device_ip_from_arp(TARGET_MAC_ADDRESS)
            if not device_ip:
                device_ip = find_device_ip_with_nmap(TARGET_MAC_ADDRESS)
            if not device_ip:
                raise socket.gaierror("Shelly IP could not be discovered with mDNS, ARP, or Nmap")
            print(f"Found Shelly IP {device_ip} in the ARP table.")
        status = send_request(f"http://{device_ip}/status", {})
        wifi_connected = status.get("wifi_sta", {}).get("connected") is True
        mqtt_connected = status.get("mqtt", {}).get("connected") is True
        print(f"Wi-Fi connected: {'yes' if wifi_connected else 'no'}.")
        print(f"MQTT connected: {'yes' if mqtt_connected else 'no'}.")
        print(f"Successfully configured the Shelly smart plug '{arguments.name}'.")
    except (ShellyApiError, WifiConnectionError, socket.gaierror) as e:
        print(f"Failed to configure the Shelly smart plug: {e}")
        exit(1)
    finally:
        print("Disconnecting from the Shelly Wi-Fi network.")
        disconnect_from_wifi()
        
if __name__ == "__main__":
    main()
    


