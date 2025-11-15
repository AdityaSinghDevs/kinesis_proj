"""Module defining the Obstacle class, which represents obstacles in the environment."""
from sim.object.sim_object import Object
from utils.vector import Vector


class Obstacle(Object):

    __slots__ = ('end')

    def __init__(self, start: Vector, end: Vector):
        super().__init__(position=start)
        self.end = end
