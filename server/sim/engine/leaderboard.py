from typing import List, Dict
from sim.object.agent import Agent

class LeaderboardManager:
    """
    Manages real-time leaderboard ranking for agents on the track.
    Sorts by: laps -> progress -> speed
    """

    def __init__(self):
        self._leaderboard: List[Dict] = []

    def update(self, agents: List[Agent]) -> None:
        # Build ranking snapshot
        self._leaderboard = sorted(
            (
                {
                    "id": a.obj_id,
                    "lap": a.lap,
                    "speed": a.speed,
                    "state": a.state,
                    "fuel": a.fuel,
                }
                for a in agents if a.state != 'crashed'
            ),
            key=lambda x: (x["lap"], x["speed"]),
            reverse=True
        )

        # Assign ranks
        for i, entry in enumerate(self._leaderboard, start=1):
            entry["rank"] = i

    def get_leaderboard(self) -> List[Dict]:
        return self._leaderboard

