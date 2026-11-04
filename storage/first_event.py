import json
import os
event = {
    "source_ip": "192.168.1.15",
    "source_port": 54321,
    "destination_port": 2222,
    "protocol": "TCP",
    "event_type": "connection_accepted"
}

print(event)



if os.path.exists("storage/events.json"):
    with open("storage/events.json", "r") as file:
        events = json.load(file)
else:
    events = []

events.append(event)

with open("storage/events.json", "w") as file:
    json.dump(events, file, indent=4)