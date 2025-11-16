from utils.vector import Vector
from utils.init_utils import create_initial_position, random_j_vector
from controllers.heuristics.spatial_hash_grid import SpatialHashGrid
from controllers.heuristics.heuristics_controller import HeuristicController
from sim.object.sim_object import Object
from sim.object.agent import Agent
from sim.object.obstacle import Obstacle
from sim.engine.world_view import WorldView

from configs.settings import DEFAULT_SEARCH_RADIUS, NUM_AGENTS, MAX_SPEED
from configs.settings import DEFAULT_CONTROLLER, SIM_TICK_RATE, NUM_OBSTACLES
from sim.engine.leaderboard import LeaderboardManager

import random
import time
import asyncio

DT = 1.0 / SIM_TICK_RATE


class SimulationEngine(WorldView):
    """Core simulation engine managing agents and obstacles."""

    __slots__ = ('_objects', '_spatial_hash_grid', 'state', 'leaderboard_manager')

    def __init__(self):
        self._objects: dict[int, Object] = {}
        self._spatial_hash_grid = SpatialHashGrid(cell_size=5.0)
        self.state: str = 'initialized'
        self.leaderboard_manager = LeaderboardManager()

    async def run(self):
        accumulator = 0.0
        prev_time = time.perf_counter()
        while self.state == 'running':
            now = time.perf_counter()
            frame_time = now - prev_time
            prev_time = now
            accumulator += frame_time

            while accumulator >= DT:
                self.update()
                accumulator -= DT

            await asyncio.sleep(0)

    def init_agents(self, num_agents: int = NUM_AGENTS, max_speed: int = MAX_SPEED) -> None:
        for i in range(num_agents):
            controller = HeuristicController(
                agent=None, world_view=self) if DEFAULT_CONTROLLER == 'heuristic' else None
            agent = Agent(
                position=create_initial_position(),
                speed=random.uniform(50, max_speed),
                direction=Vector(-1, 0),
                state='idle',
                controller=controller
            )
            if isinstance(controller, HeuristicController):
                controller.agent = agent
            self._objects[agent.obj_id] = agent
            self._spatial_hash_grid.insert(
                agent.obj_id, agent.position.x, agent.position.y)

    def init_obstacles(self, num_obstacles: int = NUM_OBSTACLES) -> None:
        for i in range(num_obstacles):
            obstacle = Obstacle(create_initial_position(), random_j_vector())
            self._objects[obstacle.obj_id] = obstacle
            self._spatial_hash_grid.insert(
                obstacle.obj_id, obstacle.position.x, obstacle.position.y)

    def update(self) -> None:
        print(self.get_agent_state());
        for obj in self._objects.values():
            if isinstance(obj, Agent):
                if (obj.state in ('crashed', 'out_of_fuel')):
                    continue
                obj.update_agent_state(DT)
                self._spatial_hash_grid.move(
                    obj.obj_id, obj.position.x, obj.position.y)
        self.leaderboard_manager.update(self._objects.values())

    def get_object_by_id(self, obj_id: int) -> Object:
        if obj_id in self._objects:
            return self._objects[obj_id]

        raise KeyError(f"Object ID {obj_id} not found in simulation.")

    def get_neighbors(self, position: Vector, radius: float = DEFAULT_SEARCH_RADIUS):
        return self._spatial_hash_grid.query_radius(position.x, position.y, radius)

    def get_agent_state(self) -> dict:
        state = []
        for obj in self._objects.values():
            if isinstance(obj, Agent):
                state.append({
                    'id': obj.obj_id,
                    'position': (obj.position.x, obj.position.y),
                    'speed': obj.speed,
                    'direction': (obj.direction.x, obj.direction.y),
                    'state': obj.state,
                    'fuel': obj.fuel,
                    'lap': obj.lap
                })
        return state

    def get_live_leaderboard(self) -> list:
        return self.leaderboard_manager.get_leaderboard()
