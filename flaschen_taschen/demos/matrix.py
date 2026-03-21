"""Matrix demo: The Matrix code rain effect.

Ported from MatrixDemo.swift - green falling lines with white heads
and fading brightness trails.
"""

import random
from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo, run_demo


class MatrixDemo(Demo):
    """The Matrix code rain effect - green falling trails with white heads."""

    def setup(self) -> None:
        """Initialize matrix state."""
        super().setup()
        assert self.canvas is not None

        # Initialize columns (Y position for head of each column)
        self.columns = [random.randint(0, self.canvas.height - 1)
                       for _ in range(self.canvas.width)]
        # Initialize brightness for each column
        self.brightness = [random.randint(100, 255)
                          for _ in range(self.canvas.width)]
        self.trail_length = 8

    def update(self) -> None:
        """Update column positions."""
        assert self.canvas is not None

        for x in range(self.canvas.width):
            self.columns[x] += 1
            if self.columns[x] >= self.canvas.height:
                self.columns[x] = 0
                self.brightness[x] = random.randint(100, 255)

    def draw(self) -> None:
        """Draw the matrix effect with trails."""
        assert self.canvas is not None

        self.canvas.clear(Color.BLACK)

        for x in range(self.canvas.width):
            # Draw trail below the head
            trail_start = max(0, self.columns[x] - self.trail_length)
            for trail_y in range(trail_start, self.columns[x]):
                dist_from_head = self.columns[x] - trail_y
                trail_brightness = max(0, self.brightness[x] - (dist_from_head * 32))
                trail_color = Color(0, trail_brightness, 0)  # Green
                self.canvas.set_pixel(x, trail_y, trail_color)

            # Draw white head
            head_color = Color(255, 255, 255)
            self.canvas.set_pixel(x, self.columns[x], head_color)


if __name__ == "__main__":
    run_demo(MatrixDemo)
