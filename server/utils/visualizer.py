import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
from matplotlib.animation import FuncAnimation
from sim.object.agent import Agent
from configs.settings import LEFT_RECT_HALF, TRACK_OUTER_RADIUS, TRACK_INNER_RADIUS, AGENT_RADIUS


class OvalVisualizer:
    """
    Simple matplotlib visualizer for the oval track and agents.
    """

    def __init__(self, rect_half: float = LEFT_RECT_HALF, r_outer: float = TRACK_OUTER_RADIUS, r_inner: float = TRACK_INNER_RADIUS):
        self.rect_half = rect_half
        self.r_outer = r_outer
        self.r_inner = r_inner

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.agents_artists = []

    # -----------------------------------------------------
    # Track drawing
    # -----------------------------------------------------
    def _draw_track(self):
        ax = self.ax
        rh, ro, ri = self.rect_half, self.r_outer, self.r_inner

        ax.set_aspect("equal", "box")

        # Outer boundary
        outer_left = Arc((-rh, 0), 2 * ro, 2 * ro, angle=0, theta1=90, theta2=270)
        outer_right = Arc((rh, 0), 2 * ro, 2 * ro, angle=0, theta1=-90, theta2=90)

        # Inner boundary
        inner_left = Arc((-rh, 0), 2 * ri, 2 * ri, angle=0, theta1=90, theta2=270)
        inner_right = Arc((rh, 0), 2 * ri, 2 * ri, angle=0, theta1=-90, theta2=90)

        # Straight segments
        ax.plot([-rh, rh], [ro, ro], "k")
        ax.plot([-rh, rh], [-ro, -ro], "k")
        ax.plot([-rh, rh], [ri, ri], "k", linestyle="--", alpha=0.5)
        ax.plot([-rh, rh], [-ri, -ri], "k", linestyle="--", alpha=0.5)

        for patch in [outer_left, outer_right, inner_left, inner_right]:
            ax.add_patch(patch)

        ax.set_xlim(-rh - ro - 2, rh + ro + 2)
        ax.set_ylim(-ro - 2, ro + 2)
        ax.set_title("Kenesis Oval Track Simulation")

    # -----------------------------------------------------
    # Agent setup
    # -----------------------------------------------------
    def init_agents(self, agents: list[Agent]):
        """Create matplotlib circles for agents."""
        self.agents_artists.clear()

        for agent in agents:
            circle = Circle(
                (agent.position.x, agent.position.y),
                AGENT_RADIUS,
                color="C0",
                alpha=0.8,
                label=f"Agent {agent.obj_id}",
            )
            self.ax.add_patch(circle)
            self.agents_artists.append(circle)

    # -----------------------------------------------------
    # Frame update
    # -----------------------------------------------------
    def update(self, agents: list[Agent]):
        """Update agent positions only."""
        for circle, agent in zip(self.agents_artists, agents):
            circle.center = (agent.position.x, agent.position.y)

    # -----------------------------------------------------
    # Run animation
    # -----------------------------------------------------
    def run(self, agents: list[Agent], update_func, steps: int = 500):
        """Run animation."""
        self._draw_track()
        self.init_agents(agents)

        def animate(_):
            update_func()
            self.update(agents)
            return self.agents_artists

        anim = FuncAnimation(self.fig, animate, frames=steps, interval=60, blit=False)
        plt.show()

