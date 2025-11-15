"""Module defining the Object class with id and position attributes."""
from utils.vector import Vector
from abc import ABC

import random


class Object(ABC):

    __slots__ = ('obj_id', 'position')

    def __init__(self, position: Vector):
        self.obj_id = random.randint(1000, 9999)
        self.position = position

    def display(self):
        return f"Object Name: {self.name}, Object Value: {self.value}"
