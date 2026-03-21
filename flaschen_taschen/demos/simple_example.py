"""Simple example demo: Draw colored rectangles on the display.

Demonstrates basic canvas operations with static colored rectangles.
Minimal CPU load, good for testing connectivity and frame rate.
"""

from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo, run_demo


class SimpleExampleDemo(Demo):
    """Draw colored rectangles in a simple grid pattern."""

    def update(self) -> None:
        """No animation, just static display."""
        pass

    def draw(self) -> None:
        """Draw colored rectangles."""
        assert self.canvas is not None

        # Clear to black
        self.canvas.clear(Color.BLACK)

        # Draw colored rectangles
        colors = [
            (Color.RED, 0, 0),
            (Color.GREEN, 10, 0),
            (Color.BLUE, 20, 0),
            (Color.YELLOW, 30, 0),
            (Color.CYAN, 0, 10),
            (Color.MAGENTA, 10, 10),
            (Color.WHITE, 20, 10),
        ]

        for color, x, y in colors:
            self.canvas.fill_rect(x, y, 9, 9, color)


if __name__ == "__main__":
    run_demo(SimpleExampleDemo)
