
import json
import os
import uuid
import ipaddress
import threading
from datetime import datetime, timezone

_write_lock = threading.Lock()


def create_event(addr, destination_port, event_type, **extra):
    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_ip": addr[0],
        "source_port": addr[1],
        "destination_port": destination_port,
        "protocol": "TCP",
        "event_type": event_type
    }

    event.update(extra)
    return event


def validate_event(event):
    required = {
        "event_id", "source_ip", "source_port",
        "destination_port", "protocol", "event_type",
        "timestamp"
    }

    if not required.issubset(event):
        return False

    try:
        ipaddress.ip_address(event["source_ip"])
    except ValueError:
        return False

    for field in ("source_port", "destination_port"):
        if (
            not isinstance(event[field], int)
            or not 1 <= event[field] <= 65535
        ):
            return False

    return event["protocol"] == "TCP"


def save_event(event):
    if not validate_event(event):
        print("Invalid event rejected!")
        return False

    with _write_lock:
        if os.path.exists("storage/events.json"):
            with open("storage/events.json", "r") as file:
                events = json.load(file)
        else:
            events = []

        events.append(event)

        with open("storage/events.json", "w") as file:
            json.dump(events, file, indent=4)

    return True
