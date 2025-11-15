import asyncio

from fastapi import FastAPI, WebSocket
import uvicorn

from sim.engine.sim_engine import SimulationEngine
from fastapi.websockets import WebSocketDisconnect

from configs.settings import TELEMETRY_TICK_RATE
from utils.logger import get_logger
from utils.visualizer import OvalVisualizer

logger = get_logger(__name__)

app = FastAPI()
sim_engine = SimulationEngine()

DT = 1.0 / TELEMETRY_TICK_RATE


@app.on_event("startup")
async def startup_event():
    """Initializes the simulation engine on startup."""
    global sim_engine
    logger.info("Starting KINESIS simulation backend")
    sim_engine.init_agents()
    logger.info(f"Simulation engine initialized with {
                len(sim_engine._objects)} agents")
    sim_engine.init_obstacles()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Streams simulation frames to the frontend."""
    await websocket.accept()
    try:
        while True:
            if sim_engine.state == 'running':
                snapshot = sim_engine.get_agent_state()
                await websocket.send_json(snapshot)
            await asyncio.sleep(DT)
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")


@app.post("/start")
async def start_simulation():
    """Starts the simulation"""
#    global sim_engine
#    if sim_engine.state != 'running':
#        sim_engine.state = 'running'
#        asyncio.create_task(sim_engine.run())
    global sim_engine
    viz = OvalVisualizer()
    viz.run(sim_engine._objects.values(), sim_engine.update)
    return {"status": "started"}


@app.post("/pause")
async def pause_simulation():
    """Pauses the simulation"""
    global sim_engine
    if sim_engine.state == 'running':
        sim_engine.state = 'paused'
    return {"status": "paused"}


@app.get("/")
def root():
    return {"status": "KINESIS simulation backend running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
