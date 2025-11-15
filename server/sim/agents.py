import random
import json
from configs.settings import NUM_AGENTS, MAX_SPEED, FUEL_USAGE, TRACK_LENGTH, LAP_LIMIT

# load zone data
try:
    track = json.load(open("config/track.json"))
except FileNotFoundError:
    track = {"zones": []}

BEHAVIORS = {
    "aggressive": {"speed_mul": 1.2, "fuel_rate": 1.3},
    "defensive": {"speed_mul": 0.8, "fuel_rate": 0.7},
    "adaptive": {"speed_mul": 1.0, "fuel_rate": 1.0}
}


def update_agent(agent, fuel_usage = FUEL_USAGE, track_length = TRACK_LENGTH):
    if agent["fuel"] <= 0 or agent["status"] != "running":
        return agent
    agent["pos"] += agent["speed"]
    b = agent["behavior"]
    agent["fuel"] -= fuel_usage * agent["speed"] * BEHAVIORS[b]["fuel_rate"]

    if agent["pos"] >= track_length:
        agent["pos"] = 0.0
        agent["lap"] += 1
    agent["total_distance"] = agent.get("total_distance", 0) + agent["speed"]

    return agent 

def apply_zone_effects(agent):
    """Applies zone modifiers to agent speed."""
    for z in track["zones"]:
        if z["start"] <= agent["pos"] <= z["end"]:
            agent["speed"] *= z["factor"]
    return agent
