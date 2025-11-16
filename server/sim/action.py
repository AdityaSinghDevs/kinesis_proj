"""Defines discrete action candidates for evaluation in a driving simulation."""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True, slots=True)
class Action:
    """Discrete action candidate for evaluation."""
    speed_factor: float  # multiply current speed by this (0..inf)
    steer_rad: float     # instantaneous rotation in radians


DEFAULT_ACTIONS: dict[str, Action] = {
    "maintain": Action(1.0, 0.0),
    "accel_soft": Action(1.05, 0.0),
    "brake_soft": Action(0.7, 0.0),
    "brake_hard": Action(0.3, 0.0),
    "steer_left": Action(0.90, np.deg2rad(6.0)),
    "steer_right": Action(0.90, -np.deg2rad(6.0)),
    "overtake_left": Action(1.15, np.deg2rad(10.0)),
    "overtake_right": Action(1.15, -np.deg2rad(10.0)),
}
