"""Simple example demo: Sets two static points on the display.

Red dot at (0,0) and blue dot at (5,5).
Minimal demo for testing connectivity and basic canvas operations.
"""

from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo, run_demo


class SimpleExampleDemo(Demo):
    """Set two static pixels on the display."""

    def update(self) -> None:
        """No animation, just static display."""
        pass

    def draw(self) -> None:
        """Set two pixels: red at (0,0) and blue at (5,5)."""
        assert self.canvas is not None

        # Set red pixel at (0,0)
        self.canvas.set_pixel(0, 0, Color.RED)

        # Set blue pixel at (5,5)
        self.canvas.set_pixel(5, 5, Color.BLUE)


if __name__ == "__main__":
    run_demo(SimpleExampleDemo)
