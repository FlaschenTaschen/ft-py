"""
NbLogo - Noisebridge logo animation
Ported from nb-logo.cc

Renders a bouncing Noisebridge logo with rainbow color cycling.
"""

from flaschen_taschen.demos import Demo
from flaschen_taschen.client.color import Color
from flaschen_taschen.standard_options import StandardOptions

LOGO_WIDTH = 16
LOGO_HEIGHT = 15

NB_LOGO = [
    "      ##.       ",
    "     #..#.      ",
    "   ###  ###.    ",
    "  #...  ...#.   ",
    "  #.      .#. #.",
    "##.      ..#.##.",
    "..###.   ####.#.",
    "###..    #..#.#.",
    "..###.   #..#.#.",
    "###..    ####.#.",
    "...## .. ..#.##.",
    "  #...##.  #..#.",
    "  #..#..#..#. . ",
    "   ###. ###.    ",
    "   ...  ...     "
]


class NbLogo(Demo):
    """
    Bouncing Noisebridge logo with rainbow color cycling.

    The demo:
    - Displays a 16x15 pixel logo bitmap
    - Bounces the logo around the screen
    - Cycles through a 256-color rainbow palette
    - Updates position every 8 frames
    """

    def __init__(self, std_opts):
        super().__init__(std_opts)
        self.frame_count = 0
        self.x = -1
        self.y = -1
        self.sx = 1  # Velocity in X
        self.sy = 1  # Velocity in Y
        self.logo_color = None  # None = use palette, otherwise fixed color

        # Parse demo-specific arguments
        args = std_opts.non_standard_args
        i = 0
        while i < len(args) and args[i].startswith('-'):
            arg = args[i]
            option = arg[1:]

            if option == 'c':
                i += 1
                if i < len(args):
                    try:
                        color_val = int(args[i], 16)
                        r = (color_val >> 16) & 0xFF
                        g = (color_val >> 8) & 0xFF
                        b = color_val & 0xFF
                        self.logo_color = Color(r, g, b)
                    except (ValueError, IndexError):
                        pass

            i += 1

    def setup(self):
        """Initialize palette."""
        super().setup()
        self.palette = self._create_palette()
        self.bg_color = Color(1, 1, 1)  # Nearly black background

    def update(self):
        """Update logo position and animation state."""
        # Animate position (move every 8 frames)
        if self.frame_count % 8 == 0:
            self.x += self.sx
            if self.x > (self.canvas.width - LOGO_WIDTH):
                self.x -= self.sx
                self.sy = 1
                self.y += self.sy
            if self.y > (self.canvas.height - LOGO_HEIGHT):
                self.y -= self.sy
                self.sx = -1
                self.x += self.sx
            if self.x < -1:
                self.x -= self.sx
                self.sy = -1
                self.y += self.sy
            if self.y < -1:
                self.y -= self.sy
                self.sx = 1
                self.x += self.sx

        self.frame_count += 1

    def draw(self):
        """Draw bouncing logo."""
        # Clear canvas
        self.canvas.fill_rect(0, 0, self.canvas.width, self.canvas.height, self.bg_color)

        # Get current color
        current_color = self.logo_color or self.palette[self.frame_count % 256]

        # Draw logo
        for logo_y in range(LOGO_HEIGHT):
            line = NB_LOGO[logo_y]
            for logo_x in range(len(line)):
                char = line[logo_x]
                screen_x = self.x + logo_x + 1
                screen_y = self.y + logo_y + 1

                if 0 <= screen_x < self.canvas.width and 0 <= screen_y < self.canvas.height:
                    if char == '#':
                        self.canvas.set_pixel(screen_x, screen_y, current_color)
                    elif char == '.':
                        self.canvas.set_pixel(screen_x, screen_y, self.bg_color)

    def _create_palette(self):
        """Generate 256-color rainbow palette."""
        palette = [Color(0, 0, 0)] * 256

        # Rainbow gradient in 8 sections of 32 colors each
        self._add_gradient(palette, 0, 31, 255, 0, 255, 0, 0, 255)        # Magenta to Blue
        self._add_gradient(palette, 32, 63, 0, 0, 255, 0, 255, 255)       # Blue to Cyan
        self._add_gradient(palette, 64, 95, 0, 255, 255, 0, 255, 0)       # Cyan to Green
        self._add_gradient(palette, 96, 127, 0, 255, 0, 127, 255, 0)      # Green to Yellow-Green
        self._add_gradient(palette, 128, 159, 127, 255, 0, 255, 255, 0)   # Yellow-Green to Yellow
        self._add_gradient(palette, 160, 191, 255, 255, 0, 255, 127, 0)   # Yellow to Orange
        self._add_gradient(palette, 192, 223, 255, 127, 0, 255, 0, 0)     # Orange to Red
        self._add_gradient(palette, 224, 255, 255, 0, 0, 255, 0, 255)     # Red to Magenta

        return palette

    @staticmethod
    def _add_gradient(palette, start, end, r1, g1, b1, r2, g2, b2):
        """Add a color gradient to the palette."""
        range_val = end - start
        for i in range(range_val + 1):
            k = i / range_val if range_val > 0 else 0
            r = int(r1 + (r2 - r1) * k)
            g = int(g1 + (g2 - g1) * k)
            b = int(b1 + (b2 - b1) * k)
            palette[start + i] = Color(r, g, b)


if __name__ == '__main__':
    from flaschen_taschen.demos import run_demo
    run_demo(NbLogo)
