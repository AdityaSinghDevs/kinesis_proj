from __future__ import annotations

from sim.object.sim_object import Object
from sim.object.agent import Agent
from sim.object.obstacle import Obstacle
from sim.engine.world_view import WorldView
from controllers.heuristics.ttc import ttc_to_boundary, ttc_to_object, ttc_to_agent
from controllers.controller import Controller
from sim.action import Action
from sim.action import DEFAULT_ACTIONS

import numpy as np
import random

from configs.settings import DEFAULT_TIME_HORIZON_LOWER, DEFAULT_TIME_HORIZON_UPPER, MAX_SPEED


class HeuristicController(Controller):

    __slot__ = ('agent_id', 'world_view',)
    _ttc_cache: dict[tuple[int, int], float] = {}

    def __init__(self, agent: Agent, world_view: WorldView) -> None:
        self.agent = agent
        self.world_view = world_view

    def predict(self) -> Action:
        bound_ttc = ttc_to_boundary(self.agent.position,
                                    self.agent.direction * self.agent.speed)

        if bound_ttc <= random.uniform(DEFAULT_TIME_HORIZON_LOWER, DEFAULT_TIME_HORIZON_UPPER):
            smallest_ttc = bound_ttc
            best_actions = self.find_best_evasive_action_for_boundary(
                ['steer_left', 'steer_right', 'maintain', 'overtake_left', 'overtake_right'])
            return DEFAULT_ACTIONS[best_actions]
        neighors: list[int] = self.world_view.get_neighbors(
            self.agent.position)
        smallest_ttc = bound_ttc
        for neighbor_id in neighors:
            if neighbor_id == self.agent.obj_id:
                continue

            neighbor_object = self.world_view.get_object_by_id(neighbor_id)
            ttc = self._compute_ttc(neighbor_object)
            if ttc <= random.uniform(DEFAULT_TIME_HORIZON_LOWER, DEFAULT_TIME_HORIZON_UPPER) and ttc < smallest_ttc:
                smallest_ttc = ttc
        if smallest_ttc == np.inf:
            if (self.agent.speed < MAX_SPEED and random.random() < 0.4):
                return DEFAULT_ACTIONS['accel_soft']
            else:
                return DEFAULT_ACTIONS['maintain']
        else:
            best_actions = self.find_best_evasive_action(smallest_ttc)
            return DEFAULT_ACTIONS[best_actions]

    def find_best_evasive_action_for_boundary(self, actions: list(str)) -> str:
        max_smallest_ttc = 0
        best_action = 'maintain'
        for action_name, action in DEFAULT_ACTIONS.items():
            if action_name not in actions:
                continue
            bound_ttc = ttc_to_boundary(
                self.agent.position,
                (self.agent.direction.rotate(action.steer_rad)
                 * self.agent.speed * action.speed_factor)
            )
            if bound_ttc <= random.uniform(DEFAULT_TIME_HORIZON_LOWER, DEFAULT_TIME_HORIZON_UPPER) and bound_ttc > max_smallest_ttc:
                max_smallest_ttc = bound_ttc
                best_action = action_name
        return best_action

    def find_best_evasive_action(self, ttc: float) -> str:
        max_smallest_ttc = 0
        min_count = np.inf
        best_action = 'maintain'
        for action_name, action in DEFAULT_ACTIONS.items():
            count = 0
            bound_ttc = ttc_to_boundary(
                self.agent.position,
                (self.agent.direction.rotate(action.steer_rad)
                 * self.agent.speed * action.speed_factor)
            )
            smallest_ttc = np.inf
            if bound_ttc <= random.uniform(DEFAULT_TIME_HORIZON_LOWER, DEFAULT_TIME_HORIZON_UPPER):
                smallest_ttc = bound_ttc
                count += 1
            neighors: list[int] = self.world_view.get_neighbors(
                self.agent.position)
            for neighbor_id in neighors:
                if neighbor_id == self.agent.obj_id:
                    continue

                neighbor_object = self.world_view.get_object_by_id(
                    neighbor_id)
                ttc = self.compute_ttc_for_action(action, neighbor_object)
                if ttc <= random.uniform(DEFAULT_TIME_HORIZON_LOWER, DEFAULT_TIME_HORIZON_UPPER):
                    smallest_ttc = ttc
                    count += 1

            if count < min_count:
                min_count = count
                best_action = action_name
        return best_action

    def compute_ttc_for_action(self, action: Action, neighbor: Object) -> float:
        if isinstance(neighbor, Obstacle):
            ttc = ttc_to_object(
                self.agent.direction.rotate(action.steer_rad)
                * self.agent.speed * action.speed_factor,
                self.agent.position,
                neighbor.position,
                neighbor.end
            )
            return ttc
        if isinstance(neighbor, Agent):
            ttc = ttc_to_agent(
                self.agent.direction.rotate(action.steer_rad)
                * self.agent.speed * action.speed_factor,
                neighbor.direction * neighbor.speed,
                self.agent.position,
                neighbor.position
            )
            return ttc

        raise ValueError("Unsupported object type for TTC computation")

    def _compute_ttc(self, obj: Object) -> float:
        if isinstance(obj, Obstacle):
            ttc = ttc_to_object(
                self.agent.direction * self.agent.speed,
                self.agent.position,
                obj.position,
                obj.end
            )
            return ttc

        if isinstance(obj, Agent):
            agent = obj
            key = (obj.obj_id, agent.obj_id)
            if key in self._ttc_cache:
                return self._ttc_cache[key]

            ttc = ttc_to_agent(
                self.agent.direction * self.agent.speed,
                obj.direction * obj.speed,
                self.agent.position,
                obj.position
            )
            key = (agent.obj_id, obj.obj_id)
            self._ttc_cache[key] = ttc
            return ttc

        raise ValueError("Unsupported object type for TTC computation")
