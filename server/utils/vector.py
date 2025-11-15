from __future__ import annotations

import sys
import numpy as np
import math
from typing import Optional

EPS = sys.float_info.epsilon


class Vector:
    """
    Lightweight 2D vector wrapper for simulation tasks.
    Internally stores values as a NumPy float64 array.
    """

    __slots__ = ("_v",)

    def __init__(self, x: float, y: float):
        self._v = np.array([float(x), float(y)], dtype=float)

    @classmethod
    def from_array(cls, arr: np.ndarray) -> Vector:
        return cls(float(arr[0]), float(arr[1]))

    @classmethod
    def zero(cls) -> Vector:
        return cls(0.0, 0.0)

    # Basic numeric accessors
    @property
    def x(self) -> float:
        return float(self._v[0])

    @property
    def y(self) -> float:
        return float(self._v[1])

    def to_array(self) -> np.ndarray:
        return self._v.copy()

    # Vector operations
    def magnitude(self) -> float:
        return float(np.linalg.norm(self._v))

    def normalized(self) -> Vector:
        mag = self.magnitude()
        if mag <= EPS:
            return Vector.zero()
        return Vector.from_array(self._v / mag)

    def dot(self, other: Vector) -> float:
        return float(np.dot(self._v, other._v))

    def distance_to(self, other: Vector) -> float:
        return float(np.linalg.norm(self._v - other._v))

    # Operators
    def __add__(self, other: Vector) -> "Vector":
        return Vector.from_array(self._v + other._v)

    def __sub__(self, other: Vector) -> "Vector":
        return Vector.from_array(self._v - other._v)

    def __mul__(self, scalar: float) -> Vector:
        return Vector.from_array(self._v * float(scalar))

    # Transformations
    def rotate(self, angle_rad: float) -> Vector:
        c = np.cos(angle_rad)
        s = np.sin(angle_rad)
        x, y = self._v
        return Vector(x * c - y * s, x * s + y * c)

    # Debug/representation
    def __repr__(self) -> str:
        return f"Vector({self.x:.4f}, {self.y:.4f})"

    def angle_between(u: Vector, v: Vector) -> Optional[float]:
        """
        Compute the unsigned angle between two vectors in radians.

        Parameters:
            u (Vector): First vector.
            v (Vector): Second vector.

        Returns:
            float | None: Angle in radians, or None if one vector is zero.
        """
        mag_u = u.magnitude()
        mag_v = v.magnitude()

        # Avoid division by zero
        if mag_u < sys.float_info.epsilon or mag_v < sys.float_info.epsilon:
            return None

        # Dot product normalized by magnitudes
        cos_theta = u.dot(v) / (mag_u * mag_v)

        # Clamp to avoid floating-point domain errors
        cos_theta = max(-1.0, min(1.0, cos_theta))

        return math.acos(cos_theta)
