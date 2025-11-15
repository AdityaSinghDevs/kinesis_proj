import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "settings.yaml")


def load_config(path=CONFIG_PATH):
    with open(path, "r") as f:
        return yaml.safe_load(f)


cfg = load_config()

NUM_AGENTS = cfg['num_agents']
FUEL_USAGE = cfg['fuel_usage']
MAX_SPEED = cfg['max_speed']
LAP_LIMIT = cfg['lap_limit']
DEFAULT_SEARCH_RADIUS = cfg['default_search_radius']
DEFAULT_CONTROLLER = cfg['default_controller']
DEFAULT_TIME_HORIZON_LOWER = cfg['default_time_horizon_lower']
DEFAULT_TIME_HORIZON_UPPER = cfg['default_time_horizon_upper']
TRACK_RECT_HALF = cfg['track_rect_half']
TRACK_INNER_RADIUS = cfg['track_inner_radius']
TRACK_OUTER_RADIUS = cfg['track_outer_radius']
SIM_TICK_RATE = cfg['sim_tick_rate']
TELEMETRY_TICK_RATE = cfg['telemetry_tick_rate']
AGENT_RADIUS = cfg['agent_radius']
NUM_OBSTACLES = cfg['num_obstacles']
