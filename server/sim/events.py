import random

def check_random_events(agents):
    global global_event
    events = []

     # occasionally trigger global slowdown
    if global_event["type"] is None and random.random() < 0.02:
        global_event = {"type": "safety_car", "timer": 5}
        events.append({"type": "safety_car", "duration": 5})

    # decrement timer
    if global_event["type"] == "safety_car":
        for a in agents:
            a["speed"] *= 0.6
        global_event["timer"] -= 1
        if global_event["timer"] <= 0:
            global_event = {"type": None, "timer": 0}


    for a in agents:
        if random.random() < 0.05 and a["status"] == "running":
            a["status"] = "crashed"
            events.append({"type" : "crash", "agent": a["id"]})
        elif a["status"] == "crashed" and random.random() < 0.3:
            a["status"] = "running"
            events.append({"type" : "recovered", "agent" : a["id"]})
    return agents, events