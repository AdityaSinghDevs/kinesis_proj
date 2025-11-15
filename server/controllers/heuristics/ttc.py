import sys
from utils.vector import Vector
import numpy as np

from configs.settings import (
    LEFT_RECT_HALF,
    TRACK_INNER_RADIUS,
    TRACK_OUTER_RADIUS,
    AGENT_RADIUS,
    RSU1_LENGTH_Y,
    RS1_LENGTH_X,
    RU_BOUND_LENGTH_X,
    RLI_BOUND1_LENGTH_Y,
    RLO_BOUND1_LENGTH_Y,
    RL_BOUND1_LENGTH_X,
    RLI_BOUND2_LENGTH_Y,
    RLO_BOUND2_LENGTH_Y,
    RLS2_LENGTH_X,
    RL_BOUND2_LENGTH_X,
    RUI_BOUND_LENGTH_Y,
    RUO_BOUND_LENGTH_Y,
)

EPS = sys.float_info.epsilon


def ttc_to_boundary(
    position: Vector,
    velocity: Vector,
) -> float:
    """
    Calculate the Time-To-Collision (TTC) for an agent moving inside a regular oval track.

    The track is rectangular in the middle (±LEFT_RECT_HALF on x-axis) with semicircular
    ends centered at (-LEFT_RECT_HALF, 0) and (+LEFT_RECT_HALF, 0).
    Boundaries are defined by inner radius (TRACK_INNER_RADIUS) and outer radius (TRACK_OUTER_RADIUS).

    Args:
        position: Vector - agent position in 2D space.
        velocity: Vector - velocity vector (direction * speed).

    Returns:
        float - Time to collision (seconds) or np.inf if no collision.
    """
    px, py = position.x, position.y
    vx, vy = velocity.x, velocity.y

    if abs(vx) <= EPS and abs(vy) <= EPS:
        return np.inf

    times: list[float] = []

    # Collision with left horizontal boundary x = -LEFT_RECT_HALF
    for y_bound in (-TRACK_INNER_RADIUS, TRACK_INNER_RADIUS, -TRACK_OUTER_RADIUS, TRACK_OUTER_RADIUS):
        # (px, py) + t * (vx, vy) = y_bound  →  py + t * vy = y_bound
        if abs(vy) > EPS:
            t = (y_bound - py) / vy
            if t > 0:
                x_at_t = px + vx * t
                if -LEFT_RECT_HALF <= x_at_t <= 0:
                    times.append(t)

    # Collision with right upper straight boundary x = RU_BOUND_LENGTH_X
    for y_bound in (RUI_BOUND_LENGTH_Y, RUO_BOUND_LENGTH_Y):
        if abs(vy) > EPS:
            t = (y_bound - py) / vy
            if t > 0:
                x_at_t = px + vx * t
                if y_bound == RUI_BOUND_LENGTH_Y and RS1_LENGTH_X <= x_at_t <= RS1_LENGTH_X + RU_BOUND_LENGTH_X:
                    times.append(t)
                if y_bound == RUO_BOUND_LENGTH_Y and RS1_LENGTH_X <= x_at_t <= RS1_LENGTH_X + RU_BOUND_LENGTH_X + 20:
                    times.append(t)

    # Collision with first right lower straight boundary x = RL_BOUND1_LENGTH_X
    for y_bound in (-RLI_BOUND1_LENGTH_Y, -RLO_BOUND1_LENGTH_Y):
        if abs(vy) > EPS:
            t = (y_bound - py) / vy
            if t > 0:
                x_at_t = px + vx * t
                if RS1_LENGTH_X <= x_at_t <= RS1_LENGTH_X + RL_BOUND1_LENGTH_X:
                    times.append(t)

    # Collision with second right lower straight boundary x = RL_BOUND2_LENGTH_X
    for y_bound in (-RLI_BOUND2_LENGTH_Y, -RLO_BOUND2_LENGTH_Y):
        if abs(vy) > EPS:
            t = (y_bound - py) / vy
            if t > 0:
                x_at_t = px + vx * t
                if RS1_LENGTH_X + RL_BOUND1_LENGTH_X + RLS2_LENGTH_X <= x_at_t <= RS1_LENGTH_X + RL_BOUND1_LENGTH_X + RLS2_LENGTH_X + RL_BOUND2_LENGTH_X:
                    times.append(t)

    # Collision with right upper slant boundary
    def _right_upper_slant_inner_ttc() -> float | None:
        # Line equation: y - (TRACK_INNER_RADIUS + RSU1_LENGTH_Y) = m * (x - RS1_LENGTH_X)
        m = RSU1_LENGTH_Y / RS1_LENGTH_X  # slope
        b = TRACK_INNER_RADIUS  # y-intercept at x=0

        a = vy - m * vx  # y intercept for velocity vector
        if abs(a) <= EPS:
            return None

        t = (m * px - py + b) / a
        if t <= EPS:
            return None

        x_at_t = px + vx * t
        if 0 <= x_at_t <= RS1_LENGTH_X:
            return t
        return None

    def _right_upper_slant_outer_ttc() -> float | None:
        # Line equation: y - (TRACK_OUTER_RADIUS + RSU1_LENGTH_Y) = m * (x - RS1_LENGTH_X)
        m = RSU1_LENGTH_Y / RS1_LENGTH_X  # slope
        b = TRACK_OUTER_RADIUS  # y-intercept at x=0

        a = vy - m * vx  # y intercept for velocity vector
        if abs(a) <= EPS:
            return None

        t = (m * px - py + b) / a
        if t <= EPS:
            return None

        x_at_t = px + vx * t
        if 0 <= x_at_t <= RS1_LENGTH_X:
            return t
        return None

    def _right_lower_slant_inner_ttc() -> float | None:
        # Line equation: y - (-RLI_BOUND1_LENGTH_Y) = m * (x - RS1_LENGTH_X)
        m = (-TRACK_INNER_RADIUS + RLI_BOUND1_LENGTH_Y) / RL_BOUND1_LENGTH_X  # slope
        b = -TRACK_INNER_RADIUS  # y-intercept at x=0

        a = vy - m * vx  # y intercept for velocity vector
        if abs(a) <= EPS:
            return None

        t = (m * px - py + b) / a
        if t <= EPS:
            return None

        x_at_t = px + vx * t
        if 0 <= x_at_t <= RS1_LENGTH_X:
            return t
        return None

    def _right_lower_slant_outer_ttc() -> float | None:
        # Line equation: y - (-RLO_BOUND1_LENGTH_Y) = m * (x - RS1_LENGTH_X)
        m = (-TRACK_OUTER_RADIUS + RLO_BOUND1_LENGTH_Y) / RL_BOUND1_LENGTH_X  # slope
        b = -TRACK_OUTER_RADIUS  # y-intercept at x=0

        a = vy - m * vx  # y intercept for velocity vector
        if abs(a) <= EPS:
            return None

        t = (m * px - py + b) / a
        if t <= EPS:
            return None

        x_at_t = px + vx * t
        if 0 <= x_at_t <= RS1_LENGTH_X:
            return t
        return None

    def _right_lower_slant2_inner_ttc() -> float | None:
        # Line equation: y - (-RLI_BOUND2_LENGTH_Y) = m * (x - (RS1_LENGTH_X + RL_BOUND1_LENGTH_X + RLS2_LENGTH_X))
        m = (-RLI_BOUND1_LENGTH_Y + RLI_BOUND2_LENGTH_Y) / RLS2_LENGTH_X  # slope
        b = -RLI_BOUND2_LENGTH_Y + m * \
            (RS1_LENGTH_X + RL_BOUND1_LENGTH_X +
             RLS2_LENGTH_X)  # y-intercept at x=0

        a = vy - m * vx  # y intercept for velocity vector
        if abs(a) <= EPS:
            return None

        t = (m * px - py + b) / a
        if t <= EPS:
            return None

        x_at_t = px + vx * t
        if RS1_LENGTH_X + RL_BOUND1_LENGTH_X <= x_at_t <= RS1_LENGTH_X + RL_BOUND1_LENGTH_X + RLS2_LENGTH_X:
            return t
        return None

    def _right_lower_slant2_outer_ttc() -> float | None:
        # Line equation: y - (-RLO_BOUND2_LENGTH_Y) = m * (x - (RS1_LENGTH_X + RL_BOUND1_LENGTH_X + RLS2_LENGTH_X))
        m = (-RLO_BOUND1_LENGTH_Y + RLO_BOUND2_LENGTH_Y) / RLS2_LENGTH_X  # slope
        b = -RLO_BOUND2_LENGTH_Y + m * \
            (RS1_LENGTH_X + RL_BOUND1_LENGTH_X +
             RLS2_LENGTH_X)  # y-intercept at x=0

        a = vy - m * vx  # y intercept for velocity vector
        if abs(a) <= EPS:
            return None

        t = (m * px - py + b) / a
        if t <= EPS:
            return None

        x_at_t = px + vx * t
        if RS1_LENGTH_X + RL_BOUND1_LENGTH_X <= x_at_t <= RS1_LENGTH_X + RL_BOUND1_LENGTH_X + RLS2_LENGTH_X:
            return t
        return None

    def right_inner_vertical_ttc() -> float | None:
        # x = RS1_LENGTH_X + RU_BOUND_LENGTH_X
        if abs(vx) <= EPS:
            return None

        t = (RS1_LENGTH_X + RU_BOUND_LENGTH_X - px) / vx
        if t <= EPS:
            return None

        y_at_t = py + vy * t
        if -RLI_BOUND2_LENGTH_Y <= y_at_t <= RUI_BOUND_LENGTH_Y:
            return t
        return None

    def right_outer_vertical_ttc() -> float | None:
        # x = RS1_LENGTH_X + RU_BOUND_LENGTH_X + 20
        if abs(vx) <= EPS:
            return None

        t = (RS1_LENGTH_X + RU_BOUND_LENGTH_X + 20 - px) / vx
        if t <= EPS:
            return None

        y_at_t = py + vy * t
        if -RLO_BOUND2_LENGTH_Y <= y_at_t <= RUO_BOUND_LENGTH_Y:
            return t
        return None

    # Collision with semicircular ends
    def _circle_ttc(center_x: float, radius: float) -> float | None:
        # Relative position
        cx = px - center_x
        cy = py

        a = vx * vx + vy * vy
        b = 2.0 * (cx * vx + cy * vy)
        c = (cx * cx + cy * cy) - radius * radius

        disc = b * b - 4.0 * a * c
        if disc < 0.0:
            return None

        sqrt_disc = np.sqrt(disc)
        t1 = (-b - sqrt_disc) / (2.0 * a)
        t2 = (-b + sqrt_disc) / (2.0 * a)

        # Valid positive intersections only
        valid = [t for t in (t1, t2) if t > EPS]
        if not valid:
            return None

        t = min(valid)
        # Must also be beyond rectangular section horizontally
        x_future = px + vx * t
        if (center_x < 0 and x_future <= -LEFT_RECT_HALF) or (center_x > 0 and x_future >= LEFT_RECT_HALF):
            return t
        return None

    for cx in (-LEFT_RECT_HALF, LEFT_RECT_HALF):
        for r in (TRACK_INNER_RADIUS, TRACK_OUTER_RADIUS):
            t_hit = _circle_ttc(cx, r)
            if t_hit is not None:
                times.append(t_hit)

    right_upper_slant_inner = _right_upper_slant_inner_ttc()
    if right_upper_slant_inner is not None:
        times.append(right_upper_slant_inner)
    right_upper_slant_outer = _right_upper_slant_outer_ttc()
    if right_upper_slant_outer is not None:
        times.append(right_upper_slant_outer)
    right_lower_slant_inner = _right_lower_slant_inner_ttc()
    if right_lower_slant_inner is not None:
        times.append(right_lower_slant_inner)
    right_lower_slant_outer = _right_lower_slant_outer_ttc()
    if right_lower_slant_outer is not None:
        times.append(right_lower_slant_outer)
    right_lower_slant2_inner = _right_lower_slant2_inner_ttc()
    if right_lower_slant2_inner is not None:
        times.append(right_lower_slant2_inner)
    right_lower_slant2_outer = _right_lower_slant2_outer_ttc()
    if right_lower_slant2_outer is not None:
        times.append(right_lower_slant2_outer)
    right_inner_vertical = right_inner_vertical_ttc()
    if right_inner_vertical is not None:
        times.append(right_inner_vertical)

    if not times:
        return np.inf

    return min(times)


def ttc_to_object(
    velocity: Vector,
    position: Vector,
    segment_start: Vector,
    segment_end: Vector
) -> float:
    """
    Time-to-collision (TTC) between a moving point and a line segment.

    Args:
        velocity: Vector, constant velocity of agent.
        position: Vector, current agent position.
        segment_start: Vector, segment start.
        segment_end: Vector, segment end.

    Returns:
        float: TTC, or np.inf if no collision.
    """
    seg_vec = segment_end - segment_start
    seg_len_sq = seg_vec.dot(seg_vec)

    if seg_len_sq <= EPS:
        return np.inf

    rel_pos = position - segment_start
    v_dot_seg = velocity.dot(seg_vec)

    if abs(v_dot_seg) <= EPS:
        return np.inf

    t = rel_pos.dot(seg_vec) / v_dot_seg
    if t < 0.0:
        return np.inf

    collision_point = position + velocity * t

    proj = (collision_point - segment_start).dot(seg_vec) / seg_len_sq

    if 0.0 - EPS <= proj <= 1.0 + EPS:
        return t

    return np.inf


def ttc_to_agent(
    v1: Vector,
    v2: Vector,
    p1: Vector,
    p2: Vector,
    radius: float = AGENT_RADIUS
) -> float:
    """
    Time-to-collision (TTC) between two moving agents (point vs point).

    Args:
        v1: Vector, velocity of agent 1.
        v2: Vector, velocity of agent 2.
        p1: Vector, position of agent 1.
        p2: Vector, position of agent 2.

    Returns:
        float: TTC or np.inf if they do not collide.
    """
    dv = v1 - v2
    dp = p1 - p2

    a = dv.dot(dv)
    if a <= EPS:
        return np.inf

    b = 2.0 * dv.dot(dp)
    c = dp.dot(dp) - radius * radius

    # solve quadratic a t^2 + b t + c = 0
    disc = b * b - 4 * a * c
    if disc < 0:
        return np.inf  # never gets within radius

    sqrt_disc = np.sqrt(disc)
    t1 = (-b - sqrt_disc) / (a * 2.0)
    t2 = (-b + sqrt_disc) / (a * 2.0)

    # we want the smallest non-negative time
    t_candidates = [t for t in (t1, t2) if t >= 0]

    if not t_candidates:
        return np.inf

    return min(t_candidates)
