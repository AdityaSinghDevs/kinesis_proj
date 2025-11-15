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
LEFT_RECT_HALF = cfg['left_rect_half']
TRACK_INNER_RADIUS = cfg['track_inner_radius']
TRACK_OUTER_RADIUS = cfg['track_outer_radius']
SIM_TICK_RATE = cfg['sim_tick_rate']
TELEMETRY_TICK_RATE = cfg['telemetry_tick_rate']
AGENT_RADIUS = cfg['agent_radius']
NUM_OBSTACLES = cfg['num_obstacles']
# right slant length x for first slant
RS1_LENGTH_X = cfg['rs1_length_x']
# right upper straight x length
RU_BOUND_LENGTH_X = cfg['ru_bound_length_x']
# right upper inner y length
RUI_BOUND_LENGTH_Y = cfg['rui_bound_length_y']
# right upper outer y length
RUO_BOUND_LENGTH_Y = cfg['ruo_bound_length_y']
# right lower straight x length for first segment
RL_BOUND1_LENGTH_X = cfg['rl_bound_length_x']
# right lower inner y length for first segment
RLI_BOUND1_LENGTH_Y = cfg['rli_bound1_length_y']
# right lower outer y length for first segment
RLO_BOUND1_LENGTH_Y = cfg['rlo_bound1_length_y']
# right lower slant length x for second slant
RLS2_LENGTH_X = cfg['rls2_length_x']
# right lower x length for second straight
RL_BOUND2_LENGTH_X = cfg['rl_bound2_length_x']
# right lower inner y length for second straight
RLI_BOUND2_LENGTH_Y = cfg['rli_bound2_length_y']
# right lower outer y length for second straight
RLO_BOUND2_LENGTH_Y = cfg['rlo_bound2_length_y']
# right upper slant length y for first slant
RSU1_LENGTH_Y = cfg['rs1_length_y']
