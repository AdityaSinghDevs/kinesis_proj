import random
from utils.vector import Vector

from configs.settings import LEFT_RECT_HALF, TRACK_INNER_RADIUS, TRACK_OUTER_RADIUS


def create_initial_position() -> Vector:
    x = random.uniform(-LEFT_RECT_HALF + 10, 0)
    y = random.uniform(TRACK_INNER_RADIUS + 15, TRACK_OUTER_RADIUS - 15)
    return Vector(x, y)


def random_j_vector() -> Vector:
    y = random.uniform(0, (TRACK_OUTER_RADIUS - TRACK_INNER_RADIUS)/3)
    return Vector(0, y)
