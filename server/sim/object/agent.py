"""Module defining the Agent class."""
from sim.object.sim_object import Object
from utils.vector import Vector
from sim.action import Action
from controllers.controller import Controller

from math import sin, cos
import random
import numpy as np

DEG2RAD = np.pi / 180.0
BIAS_ANGLE_RANGE = 3.0 * DEG2RAD

class Agent(Object):

    __slots__ = ('speed', 'direction', 'state',
                 'controller', 'fuel', 'lap')

    def __init__(self, position: Vector,
                 speed: float, direction: Vector, state: str, controller: Controller) -> None:
        super().__init__(position=position)
        self.speed = speed
        self.direction = direction.normalized()
        self.fuel = 100.0
        self.state = state
        self.lap = 0
        self.controller = controller

    def update_agent_state(self, dt: float) -> None:
        """Update the agent's state based on controller prediction."""
        if(self.state == 'crashed' or self.state == 'out_of_fuel'):
            return
        self.fuel -= self.speed * dt
        action: Action = self.controller.predict()

        if self.state in ('crashed', 'out_of_fuel'):
            # Ensure we don't move after crash/out_of_fuel
            self.speed = 0.0
            return
        print(f"[UPDATE] Updating Agent {id(self)}")
        self.speed = self.speed * action.speed_factor
        # Update direction based on steering angle
        angle = action.steer_rad
        new_direction_x = (self.direction.x * cos(angle) -
                           self.direction.y * sin(angle))
        new_direction_y = (self.direction.x * sin(angle) +
                           self.direction.y * cos(angle))
        self.direction = Vector(new_direction_x, new_direction_y).normalized()
        self.position += self.direction * self.speed * dt
        if self.speed > 0 and self.fuel > 0:
            self.state = 'moving'
        elif self.fuel == 0:
            self.state = 'out_of_fuel'
        elif self.speed == 0:
            self.state = 'stopped'
        else:
            self.state = 'idle'
