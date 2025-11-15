from collections import defaultdict
from typing import Dict, List, Tuple, Any, Iterable
import math


class SpatialHashGrid:
    """
    Uniform spatial hash grid for broad-phase neighbor queries.
    Stores objects by ID and their positions.

    Each object must have:
        - a unique key (agent_id)
        - a 2D position (x, y)

    The grid supports:
        - insertion
        - removal
        - moving objects
        - querying nearby objects within a radius

    Suitable for real-time simulations.
    """

    __slots__ = ('cell_size', 'cells', 'object_cells')

    def __init__(self, cell_size: float = 5.0):
        """
        Initialize the spatial hash grid.

        Args:
            cell_size: Size of each grid cell in world units (meters).
                       Smaller values = more precision but more cells.
        """
        self.cell_size = cell_size
        self.cells: Dict[Tuple[int, int], List[Any]] = defaultdict(list)
        self.object_cells: Dict[int, Tuple[int, int]] = {}

    def _cell_key(self, x: float, y: float) -> Tuple[int, int]:
        """Return the integer cell coordinates for a world position."""
        return (
            int(math.floor(x / self.cell_size)),
            int(math.floor(y / self.cell_size))
        )

    def insert(self, obj_id: int, x: float, y: float) -> None:
        """
        Insert an object into the grid.

        Args:
            obj_id: Unique identifier (e.g., agent_id).
            x: X coordinate of the object.
            y: Y coordinate of the object.
        """
        key = self._cell_key(x, y)
        self.cells[key].append(obj_id)
        self.object_cells[obj_id] = key

    def remove(self, obj_id: int) -> None:
        """
        Remove an object from the grid.

        Args:
            obj_id: Unique identifier of the object to remove.
        """
        if obj_id not in self.object_cells:
            return

        key = self.object_cells[obj_id]
        cell_list = self.cells[key]

        if obj_id in cell_list:
            cell_list.remove(obj_id)

        del self.object_cells[obj_id]

    def move(self, obj_id: int, new_x: float, new_y: float) -> None:
        """
        Update the grid location of an existing object.

        Args:
            obj_id: Unique identifier.
            new_x: New X coordinate.
            new_y: New Y coordinate.
        """
        old_key = self.object_cells.get(obj_id)
        new_key = self._cell_key(new_x, new_y)

        if old_key != new_key:
            # Remove from old cell
            if old_key is not None:
                cell_list = self.cells[old_key]
                if obj_id in cell_list:
                    cell_list.remove(obj_id)

            # Add to new cell
            self.cells[new_key].append(obj_id)
            self.object_cells[obj_id] = new_key

    def query_radius(self, x: float, y: float, radius: float) -> Iterable[Any]:
        """
        Return all object IDs within a given radius of a point.
        Broad-phase only; user should perform precise distance checks.

        Args:
            x: Query point X.
            y: Query point Y.
            radius: Search radius.

        Returns:
            Iterable of object IDs that may be within the radius.
        """
        cell_radius = int(math.ceil(radius / self.cell_size))
        cx, cy = self._cell_key(x, y)

        candidates: List[Any] = []

        for dx in range(-cell_radius, cell_radius + 1):
            for dy in range(-cell_radius, cell_radius + 1):
                cell_key = (cx + dx, cy + dy)
                if cell_key in self.cells:
                    candidates.extend(self.cells[cell_key])

        return candidates

    def get_cell_contents(self, x: float, y: float) -> Iterable[Any]:
        """
        Return all object IDs in the same grid cell as the given position.
        Useful for debugging.

        Args:
            x: World X coordinate.
            y: World Y coordinate.

        Returns:
            Iterable of object IDs in the same cell.
        """
        key = self._cell_key(x, y)
        return self.cells.get(key, [])

