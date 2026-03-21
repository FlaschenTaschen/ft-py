"""Quilt demo: Quilt pattern animation with mirrored symmetry.

Ported from QuiltDemo.swift - draws mirrored patterns with random colors,
incrementally building a symmetric quilt pattern.
"""

import random
from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo, run_demo

SKIP_NUM = 5


class QuiltDemo(Demo):
    """Animated quilt pattern with 4x mirrored symmetry."""

    def setup(self) -> None:
        """Initialize quilt animation state."""
        super().setup()
        assert self.canvas is not None

        # Current drawing position and color
        self.current_color = self._random_color()
        self.current_x1 = random.randint(0, SKIP_NUM - 1)
        self.current_y1 = random.randint(0, SKIP_NUM - 1)
        self.current_x = self.current_x1
        self.current_y = self.current_y1

    def update(self) -> None:
        """Update drawing position (step through grid)."""
        assert self.canvas is not None

        self.current_x += SKIP_NUM
        if self.current_x >= self.canvas.width:
            self.current_x = self.current_x1
            self.current_y += SKIP_NUM
            if self.current_y >= self.canvas.height:
                # Pattern complete, pick new color and offset
                self.current_color = self._random_color()
                self.current_x1 = random.randint(0, SKIP_NUM - 1)
                self.current_y1 = random.randint(0, SKIP_NUM - 1)
                self.current_x = self.current_x1
                self.current_y = self.current_y1

    def draw(self) -> None:
        """Draw one group of 8 mirrored pixels."""
        assert self.canvas is not None

        w = self.canvas.width
        h = self.canvas.height

        # Draw 8 mirrored pixels (4x symmetry: horiz + vert + diagonal)
        self.canvas.set_pixel(self.current_x, self.current_y, self.current_color)
        self.canvas.set_pixel(w - 1 - self.current_x, self.current_y, self.current_color)
        self.canvas.set_pixel(self.current_x, h - 1 - self.current_y, self.current_color)
        self.canvas.set_pixel(w - 1 - self.current_x, h - 1 - self.current_y, self.current_color)

        self.canvas.set_pixel(self.current_y, self.current_x, self.current_color)
        self.canvas.set_pixel(w - 1 - self.current_y, self.current_x, self.current_color)
        self.canvas.set_pixel(self.current_y, h - 1 - self.current_x, self.current_color)
        self.canvas.set_pixel(w - 1 - self.current_y, h - 1 - self.current_x, self.current_color)

    @staticmethod
    def _random_color() -> Color:
        """Generate random color."""
        return Color(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )


if __name__ == "__main__":
    run_demo(QuiltDemo)
