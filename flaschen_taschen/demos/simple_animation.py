"""Simple animation demo: Animated moving shapes.

Demonstrates time-based animation with shapes moving across the display.
Pure Python with minimal CPU overhead.
"""

import math
from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo, run_demo


class SimpleAnimationDemo(Demo):
    """Animate colored circles moving across the display."""

    def setup(self) -> None:
        """Initialize animation state."""
        super().setup()
        self.time = 0.0

    def update(self) -> None:
        """Update animation state."""
        self.time += 0.016  # ~60 FPS step

    def draw(self) -> None:
        """Draw animated circles."""
        assert self.canvas is not None

        self.canvas.clear(Color.BLACK)

        # Multiple circles with different speeds
        for i in range(3):
            # X position cycles across screen
            x = int((self.canvas.width * (self.time + i * 0.5)) % self.canvas.width)
            # Y position cycles vertically with different frequency
            y = int(
                self.canvas.height // 2 +
                (self.canvas.height // 4) * math.sin(self.time * (1 + i * 0.5))
            )

            # Cycle through colors
            colors = [Color.RED, Color.GREEN, Color.BLUE]
            color = colors[i % len(colors)]

            # Draw circle (size 3)
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    if dx*dx + dy*dy <= 9:  # Circle radius ~3
                        self.canvas.set_pixel(x + dx, y + dy, color)


if __name__ == "__main__":
    run_demo(SimpleAnimationDemo)
