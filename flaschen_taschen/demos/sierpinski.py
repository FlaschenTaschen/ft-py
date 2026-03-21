"""
Sierpinski - Sierpinski's Triangle fractal
Ported from sierpinski.cc by Carl Gorringe

Uses the "chaos game" algorithm to generate the Sierpinski triangle.
Iteratively picks a random vertex of the triangle and moves halfway
from the current point toward it, accumulating points to reveal the pattern.
"""

import random
from flaschen_taschen.demos import Demo
from flaschen_taschen.client.color import Color
from flaschen_taschen.standard_options import StandardOptions


class Sierpinski(Demo):
    """
    Sierpinski triangle fractal using the chaos game algorithm.

    The algorithm works by:
    1. Starting with a random point
    2. Each iteration: pick a random triangle vertex, move halfway toward it
    3. Mark the new point
    4. The accumulated points naturally form the Sierpinski triangle pattern

    Colors cycle through a 256-color rainbow palette by default, or
    use a fixed foreground color if specified.
    """

    def __init__(self, std_opts):
        super().__init__(std_opts)
        self.palette_mode = True
        self.fg_color = Color(0, 0, 0)  # Black by default
        self.bg_color = Color(1, 1, 1)  # Nearly black by default (matches Swift)

        # Parse demo-specific arguments
        args = std_opts.non_standard_args
        i = 0
        while i < len(args) and args[i].startswith('-'):
            arg = args[i]
            option = arg[1:]

            if option == 'c':
                i += 1
                if i < len(args):
                    color = self._parse_hex_color(args[i])
                    if color is not None:
                        self.fg_color = color
                        self.palette_mode = False
            elif option == 'b':
                i += 1
                if i < len(args):
                    color = self._parse_hex_color(args[i])
                    if color is not None:
                        self.bg_color = color

            i += 1

    def setup(self):
        """Initialize sierpinski state and palette."""
        super().setup()

        # Pixel accumulation buffer: 0=empty, 1=has point
        self.pixels = [0] * (self.canvas.width * self.canvas.height)

        # Create 256-color rainbow palette for cycling
        self.palette = self._create_rainbow_palette()
        self.color_index = 0

        # Chaos game: triangle vertices in normalized coordinates (0-1)
        # Top vertex at (0.5, 1.0), bottom-left at (0.0, 0.0), bottom-right at (1.0, 0.0)
        self.vertices = [(0.5, 1.0), (0.0, 0.0), (1.0, 0.0)]

        # Start at center of triangle (centroid) for faster visual convergence
        # Centroid = (v1 + v2 + v3) / 3 = ((0.5 + 0 + 1) / 3, (1 + 0 + 0) / 3) = (0.5, 0.333)
        self.sx = 0.5
        self.sy = 1.0 / 3.0

    def update(self):
        """Generate one step of the Sierpinski triangle."""
        # Pick random vertex
        vx, vy = random.choice(self.vertices)

        # Move halfway from current point to vertex
        self.sx = (self.sx + vx) / 2.0
        self.sy = (self.sy + vy) / 2.0

        # Convert to pixel coordinates
        # X: normalize to display width
        sxp = int((self.canvas.width - 1) * self.sx)
        # Y: normalize to display height, flip vertically (inverted Y-axis)
        syp = self.canvas.height - int((self.canvas.height - 1) * self.sy) - 1

        # Mark pixel if within bounds
        if 0 <= sxp < self.canvas.width and 0 <= syp < self.canvas.height:
            self.pixels[syp * self.canvas.width + sxp] = 1

    def draw(self):
        """Render the accumulated Sierpinski triangle to canvas."""
        # Determine current drawing color
        if self.palette_mode:
            draw_color = self.palette[self.color_index]
            self.color_index = (self.color_index + 1) % 256
        else:
            draw_color = self.fg_color

        # Copy pixel buffer to canvas
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                pixel_idx = y * self.canvas.width + x
                pixel_value = self.pixels[pixel_idx]

                color = draw_color if pixel_value != 0 else self.bg_color
                self.canvas.set_pixel(x, y, color)

    @staticmethod
    def _parse_hex_color(color_str):
        """Parse hex color string like 'ff0000' or '0'."""
        try:
            if color_str == '0':
                return None  # Transparent
            color_int = int(color_str, 16)
            r = (color_int >> 16) & 0xFF
            g = (color_int >> 8) & 0xFF
            b = color_int & 0xFF
            return Color(r, g, b)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _create_rainbow_palette():
        """Create a 256-color rainbow palette."""
        palette = []

        # Define color gradient segments
        segments = [
            (0, 31, 255, 0, 255, 0, 0, 255),      # Magenta to Blue
            (32, 63, 0, 0, 255, 0, 255, 255),    # Blue to Cyan
            (64, 95, 0, 255, 255, 0, 255, 0),    # Cyan to Green
            (96, 127, 0, 255, 0, 127, 255, 0),   # Green to Yellow-green
            (128, 159, 127, 255, 0, 255, 255, 0), # Yellow-green to Yellow
            (160, 191, 255, 255, 0, 255, 127, 0), # Yellow to Orange
            (192, 223, 255, 127, 0, 255, 0, 0),   # Orange to Red
            (224, 255, 255, 0, 0, 255, 0, 255),   # Red to Magenta
        ]

        for start, end, r1, g1, b1, r2, g2, b2 in segments:
            Sierpinski._add_gradient(palette, start, end, r1, g1, b1, r2, g2, b2)

        return palette

    @staticmethod
    def _add_gradient(palette, start, end, r1, g1, b1, r2, g2, b2):
        """Add a color gradient to the palette."""
        range_val = end - start
        for i in range(range_val + 1):
            k = i / range_val
            r = int(r1 + (r2 - r1) * k)
            g = int(g1 + (g2 - g1) * k)
            b = int(b1 + (b2 - b1) * k)
            palette.append(Color(r, g, b))


if __name__ == '__main__':
    from flaschen_taschen.demos import run_demo
    run_demo(Sierpinski)
