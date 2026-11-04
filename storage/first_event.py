import json
import os
from datetime import datetime, timezone
import uuid
import ipaddress

def validate_event(event):
    required = {"event_id", "source_ip", "source_port",
                "destination_port", "protocol", "event_type", "timestamp"}

    if not required.issubset(event):
        return False

    try:
        ipaddress.ip_address(event["source_ip"])
    except ValueError:
        return False

    for field in ("source_port", "destination_port"):
        if not isinstance(event[field], int) or not 1 <= event[field] <= 65535:
            return False

    return event["protocol"] == "TCP"

event = {
    "event_id": str(uuid.uuid4()),
    "source_ip": "192.168.1.15",
    "source_port": 54321,
    "destination_port": 2222,
    "protocol": "TCP",
    "event_type": "connection_accepted",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}


print(event)



if os.path.exists("storage/events.json"):
    with open("storage/events.json", "r") as file:
        events = json.load(file)
else:
    events = []

if validate_event(event):
    events.append(event)
else:
    print("Invalid event rejected!")

with open("storage/events.json", "w") as file:
    json.dump(events, file, indent=4)

test_event = event.copy()
test_event["source_port"] = 99999
print(validate_event(test_event))