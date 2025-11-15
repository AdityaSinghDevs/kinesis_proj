import json, time
from sim.agents import init_agents
from sim.engine import simulate_step, config

state = {"frame": 0, "agents": init_agents(config["num_agents"])}

for i in range(10):
    snapshot = simulate_step(state)
    print(json.dumps(snapshot, indent=2))
    if snapshot["events"]:
        print(f"Frame {snapshot['frame']} → {snapshot['events']}")
    time.sleep(0.2)
