"""Module defining the abstract base class for a world view."""

from abc import ABC, abstractmethod
from utils.vector import Vector


class WorldView(ABC):
    """Abstract base class representing a world view."""

    @abstractmethod
    def get_object_by_id(self, obj_id: int):
        """Retrieve an object by its ID."""
        pass

    @abstractmethod
    def get_neighbors(self, position: Vector, radius: float):
        """Retrieve neighboring objects within a certain radius."""
        pass
