# KINESIS: Competitive Mobility Systems Simulator

## Inspiration

Formula E doesn't just test speed , it tests decision-making under uncertainty. Pit strategy, energy management, overtaking windows ... every race is a high-stakes optimization problem played out in real-time. We realized that the same dynamics apply everywhere: delivery drones navigating cities, autonomous fleets coordinating routes, even traffic systems adapting to congestion.

The question wasn't "can we simulate racing?" , it was "can we build a platform where competitive motion becomes a playground for strategy?" Traditional simulators are either too complex to iterate on or too rigid to generalize. We wanted something that could model Formula E today and last-mile logistics tomorrow, without rewriting the engine.

KINESIS exists because we believe the future of mobility isn't about individual agents getting faster, it's about systems learning to compete, adapt, and optimize under pressure.

## What It Does

KINESIS is a real-time multi-agent simulation platform that models competitive mobility scenarios. At its core: agents move through dynamic environments, make strategic decisions, and compete for optimal performance.

**The system includes:**

- **Multi-agent dynamics**: 20-30 agents navigating shared space with collision detection, position tracking, and event-driven state changes
- **Event system**: Weather shifts, speed zones, pit stops, and crashes that force agents to adapt mid-race
- **Dual control architecture**: Rule-based heuristic controllers for baseline performance and reinforcement learning agents trained through simulation to discover emergent strategies
- **Real-time telemetry**: Live leaderboard, agent-level metrics, and event logging streamed at 10Hz via WebSocket
- **Modular design**: Swap track layouts, adjust agent count, inject custom events, the simulation adapts without structural changes

The output isn't just a racing game ... it's a testbed for competitive decision-making. Replace cars with drones, tracks with city grids, lap times with delivery throughput. The engine stays the same; the problem changes.

## How We're Going to Build It

**Architecture**: Three-layer separation for parallel development and clean integration.

**Simulation Engine** (Python)  
Grid-based world representation with discrete tiles for rapid prototyping, upgradeable to continuous physics if time permits. Agents maintain state (position, velocity, fuel, lap count) and update every tick based on control inputs. Events trigger through a centralized system that monitors collisions, boundary violations, and strategic actions like pit stops.

Pathfinding uses A* for optimal routing. Heuristic controllers implement rule-based decision trees: accelerate on straights, brake before turns, avoid nearby agents, pit when fuel drops below threshold. This guarantees stable baseline behavior.

**Reinforcement Learning Layer**  
We're wrapping the simulation as a Gymnasium environment with state observations (agent speed, distance to finish, nearby obstacles, track curvature), continuous actions (throttle, brake, steering), and reward shaping that balances progress, collision avoidance, and fuel efficiency.

Training runs overnight using Proximal Policy Optimization via stable-baselines3. The RL agent won't replace heuristics but it'll compete *against* them, creating a live showcase of learned strategy versus engineered rules.

**API & Streaming** (FastAPI + WebSocket)  
Backend runs the simulation loop in a background thread, exposing REST endpoints for control (start, pause, reset, trigger events) and a WebSocket broadcaster that streams state snapshots to the frontend every 100ms. This decouples simulation logic from presentation, letting the frontend consume telemetry without touching physics.

**Dashboard** (React + Canvas)  
Component-based UI with Canvas rendering for agent positions and SVG overlays for track boundaries. WebSocket client maintains synchronized state. Leaderboard sorts by position and lap time. Event log displays recent actions. Controls allow manual intervention (speed up simulation, inject weather events, spotlight individual agents).

## Challenges We Might Run Into

**Collision detection at scale**: Naive pairwise checks become O(n²) bottlenecks. We'll use spatial hashing to partition the grid and only check nearby agents, keeping performance linear as agent count grows.

**RL training instability**: Reward shaping is fragile. If progress rewards dominate too much, agents ignore fuel efficiency. If collision penalties are too harsh, they never learn aggressive overtaking. We're planning ablation runs with multiple reward configurations and picking the most balanced policy.

**WebSocket latency under load**: Broadcasting full state snapshots 10 times per second could saturate connections. If profiling shows bottlenecks, we'll switch to delta encoding (only send changed agent states) or reduce update frequency for non-critical telemetry.

**Real-time rendering performance**: Canvas redraws for 30 agents at 60fps might stutter on weaker hardware. We're implementing frame skipping (visual updates can lag behind simulation ticks without breaking logic) and culling off-screen agents from render loops.

**Demo resilience**: WiFi dies, live demos crash. We will be recording a backup video during hackathon, testing on battery power, and ensuring the entire stack runs locally with zero external dependencies. If the WebSocket fails during judging, we can fall back to pre-recorded telemetry playback.

**Scope creep**: 3D graphics, cloud deployment, multiplayer are all tempting, all deadly for a 24 Hours sprint. We're anchoring to a core deliverable (working sim + live leaderboard + one RL agent) and treating everything else as optional polish.

## Built With

**Simulation & AI**  
- Python 3.10+ for core logic and control systems  
- NumPy for efficient state array operations  
- Gymnasium for standardized RL environment interface  
- stable-baselines3 (PPO implementation) for policy training  
- NetworkX for graph-based pathfinding  

**Backend & API**  
- FastAPI for REST endpoints and WebSocket server  
- Uvicorn as ASGI server  
- asyncio for concurrent simulation loop management  

**Frontend & Visualization**  
- React 18 for component architecture  
- Vite for fast bundling and hot module replacement  
- Canvas API for agent rendering  
- SVG for static track overlays  
- Tailwind CSS for rapid styling  
- Axios for REST client  
- Native WebSocket API for telemetry streaming  

**Infrastructure**  
- Git for version control with feature-branch workflow  
- Bash scripts for one-command setup and deployment  
- YAML for configuration management  


----------------
You can also use pipreqs
 (highly recommended for hackathons):

pip install pipreqs
pipreqs . --force

---------------
ws://127.0.0.1:8000/ws