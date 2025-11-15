import json
import os

os.makedirs("telemetry", exist_ok=True)

def save_telemetry(frames, path="telemetry/demo.json"):
    """Save simulation telemetry to a JSON file for playback or analysis."""
    with open(path, "w") as f:
        json.dump(frames, f, indent=2)
