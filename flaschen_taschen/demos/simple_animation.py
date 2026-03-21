"""Simple animation demo: Animated space invaders.

Demonstrates sprite-based animation with patterns moving across the display.
Ported from ft-swift SimpleAnimationDemo.
"""

from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo, run_demo


# Space invader patterns - '#' represents a pixel to draw
INVADER_PATTERNS = [
    [
        "  #     #  ",
        "   #   #   ",
        "  #######  ",
        " ## ### ## ",
        "###########",
        "# ####### #",
        "# #     # #",
        "  ##   ##  ",
    ],
    [
        "  #     #  ",
        "#  #   #  #",
        "# ####### #",
        "### ### ###",
        " ######### ",
        "  #######  ",
        "  #     #  ",
        " #       #",
    ],
]


class SimpleAnimationDemo(Demo):
    """Animate space invaders moving across the display."""

    def setup(self) -> None:
        """Initialize animation state."""
        super().setup()
        self.frame_count = 0
        self.animation_x = 0
        self.animation_y = 0
        self.animation_direction = 1
        self.update_counter = 0

    def update(self) -> None:
        """Update animation state."""
        self.update_counter += 1
        # Update every ~300ms (assuming 10ms per update call)
        # Adjust divisor based on actual frame timing
        if self.update_counter >= 30:
            self.update_counter = 0
            self.frame_count += 1

            # Update movement on even frames
            if self.frame_count % 2 == 0:
                self.animation_x += self.animation_direction

                # Bounce logic
                if self.animation_x > 20:
                    self.animation_direction = -1
                    self.animation_y += 1
                if self.animation_x < 1:
                    self.animation_direction = 1
                    self.animation_y += 1

                # Reset Y when at max
                if self.animation_y >= 20:
                    self.animation_y = 0

    def draw(self) -> None:
        """Draw animated space invader sprite."""
        assert self.canvas is not None

        self.canvas.clear(Color.BLACK)

        # Select frame (alternates between two invader patterns)
        frame_index = self.frame_count % len(INVADER_PATTERNS)
        pattern = INVADER_PATTERNS[frame_index]

        # Alternate colors: yellow and magenta
        colors = [Color(255, 255, 0), Color(255, 0, 255)]
        color = colors[frame_index % len(colors)]

        # Draw sprite from pattern
        for dy, row in enumerate(pattern):
            for dx, char in enumerate(row):
                if char == "#":
                    x = self.animation_x + dx
                    y = self.animation_y + dy
                    self.canvas.set_pixel(x, y, color)


if __name__ == "__main__":
    run_demo(SimpleAnimationDemo)
