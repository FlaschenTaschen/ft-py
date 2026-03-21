"""
RandomDots - Random colored dots at random positions
Ported from random-dots.cc by Carl Gorringe

Continuously displays randomly colored pixels at random positions on the display.
Simple particle-like effect with no motion or physics—just pure randomness.
"""

import random
from flaschen_taschen.demos import Demo
from flaschen_taschen.client.color import Color
from flaschen_taschen.standard_options import StandardOptions


class RandomDots(Demo):
    """
    Random colored dots animation.

    Each frame:
    - Picks a random color (R, G, B each 0-255)
    - Picks a random position on the canvas
    - Draws a pixel at that position
    - Sends to display

    This creates a continuous, static (non-moving) particle effect.
    """

    def __init__(self, std_opts):
        super().__init__(std_opts)

    def setup(self):
        """Initialize canvas."""
        super().setup()
        # Clear display on startup
        self.canvas.clear()

    def update(self):
        """Random dots don't need explicit update—drawing handles everything."""
        pass

    def draw(self):
        """Draw a random dot at a random position with random color."""
        # Pick random color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)

        # Pick random position
        x = random.randint(0, self.canvas.width - 1)
        y = random.randint(0, self.canvas.height - 1)

        # Draw pixel
        self.canvas.set_pixel(x, y, color)


if __name__ == '__main__':
    from flaschen_taschen.demos import run_demo
    run_demo(RandomDots)
