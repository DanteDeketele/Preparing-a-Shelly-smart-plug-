"""Small helper for sending JSON requests to a Shelly device."""

from __future__ import annotations

import json
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class ShellyApiError(RuntimeError):
    """Raised when a Shelly API request cannot be completed or decoded."""


def send_request(url: str, body: dict[str, Any], retries: int = 5) -> dict[str, Any]:
    """Send Gen1 form parameters and return the Shelly JSON response."""
    request = Request(
        url,
        data=urlencode(body).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urlopen(request, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
            break
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            if attempt == retries:
                raise ShellyApiError(f"Shelly API request failed: {error}") from error
            time.sleep(1)
    else:
        raise ShellyApiError(f"Shelly API request failed: {last_error}")

    if not isinstance(result, dict):
        raise ShellyApiError("Shelly API returned a JSON value instead of an object")

    return result


def reboot_device(base_url: str, delay_ms: int = 1000) -> dict[str, Any]:
    """Ask a Gen1 Shelly to reboot after the request has been received."""
    return send_request(
        f"{base_url.rstrip('/')}/reboot",
        {},
    )