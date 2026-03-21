"""Black demo: Clear the display to black and keep it black.

Minimal demo for testing connectivity. Just fills the display with black.
"""

from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo, run_demo


class BlackDemo(Demo):
    """Fill display with black color."""

    def update(self) -> None:
        """No animation."""
        pass

    def draw(self) -> None:
        """Clear to black."""
        assert self.canvas is not None
        self.canvas.clear(Color.BLACK)


if __name__ == "__main__":
    run_demo(BlackDemo)
