"""Firefly demo: Wandering particles with trails.

Demonstrates particle system with simple physics and fading trails.
Pure Python, minimal CPU overhead for RPi compatibility.
"""

import random
import math
from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo, run_demo


class Firefly:
    """A single wandering firefly particle."""

    def __init__(self, x: float, y: float, width: int, height: int):
        """Initialize firefly at position.

        Args:
            x: Starting X position
            y: Starting Y position
            width: Canvas width
            height: Canvas height
        """
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.width = width
        self.height = height
        self.brightness = 255
        self.trail = []  # List of (x, y, brightness) tuples

    def update(self) -> None:
        """Update firefly position with simple physics."""
        # Add small random wander
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)

        # Limit velocity
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 2:
            self.vx = (self.vx / speed) * 2
            self.vy = (self.vy / speed) * 2

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Bounce off edges
        if self.x < 0 or self.x >= self.width:
            self.vx *= -1
            self.x = max(0, min(self.width - 1, self.x))

        if self.y < 0 or self.y >= self.height:
            self.vy *= -1
            self.y = max(0, min(self.height - 1, self.y))

        # Add to trail
        self.trail.append((int(self.x), int(self.y), self.brightness))

        # Keep trail length bounded
        if len(self.trail) > 20:
            self.trail.pop(0)

        # Pulse brightness
        self.brightness = int(128 + 127 * math.sin(random.random() * math.pi))


class FireflyDemo(Demo):
    """Wandering firefly particles with trails."""

    def setup(self) -> None:
        """Initialize fireflies."""
        super().setup()
        assert self.canvas is not None

        self.fireflies = []
        num_fireflies = 5

        for _ in range(num_fireflies):
            x = random.uniform(0, self.canvas.width)
            y = random.uniform(0, self.canvas.height)
            firefly = Firefly(x, y, self.canvas.width, self.canvas.height)
            self.fireflies.append(firefly)

    def update(self) -> None:
        """Update all fireflies."""
        for firefly in self.fireflies:
            firefly.update()

    def draw(self) -> None:
        """Draw fireflies and their trails."""
        assert self.canvas is not None

        self.canvas.clear(Color.BLACK)

        # Draw each firefly with trail
        colors = [
            Color(255, 200, 0),    # Gold
            Color(0, 255, 150),    # Cyan-green
            Color(255, 100, 255),  # Magenta
            Color(100, 150, 255),  # Blue
            Color(255, 150, 100),  # Orange
        ]

        for i, firefly in enumerate(self.fireflies):
            color = colors[i % len(colors)]

            # Draw fading trail
            for trail_idx, (tx, ty, brightness) in enumerate(firefly.trail):
                # Fade brightness along trail
                trail_brightness = int(brightness * (trail_idx / len(firefly.trail)))
                trail_color = Color(
                    int(color.r * trail_brightness / 255),
                    int(color.g * trail_brightness / 255),
                    int(color.b * trail_brightness / 255),
                )

                if 0 <= tx < self.canvas.width and 0 <= ty < self.canvas.height:
                    self.canvas.set_pixel(tx, ty, trail_color)

            # Draw firefly (bright) at current position
            fx, fy = int(firefly.x), int(firefly.y)
            if 0 <= fx < self.canvas.width and 0 <= fy < self.canvas.height:
                bright_color = Color(
                    min(255, color.r + 50),
                    min(255, color.g + 50),
                    min(255, color.b + 50),
                )
                self.canvas.set_pixel(fx, fy, bright_color)

                # Draw small bright halo
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        hx, hy = fx + dx, fy + dy
                        if 0 <= hx < self.canvas.width and 0 <= hy < self.canvas.height:
                            halo = Color(
                                color.r // 2,
                                color.g // 2,
                                color.b // 2,
                            )
                            self.canvas.set_pixel(hx, hy, halo)


if __name__ == "__main__":
    run_demo(FireflyDemo)
