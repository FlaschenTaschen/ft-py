"""
SfLogo - Sequoia Fabrica logo animation
Ported from sf-logo.cc (SVG-based tree logo)

Renders a bouncing tree logo with line-based drawing and rainbow color cycling.
"""

from flaschen_taschen.demos import Demo
from flaschen_taschen.client.color import Color
from flaschen_taschen.standard_options import StandardOptions

SF_LOGO_WIDTH = 24
SF_LOGO_HEIGHT = 34

# SVG to pixel scale factors
SVG_SCALE_X = 24.0 / 11.811159
SVG_SCALE_Y = 34.0 / 16.708437
SVG_OFFSET_X = 99.218739
SVG_OFFSET_Y = 140.22917

# Trunk lines (3 horizontal lines in lower section)
TRUNK_LINES = [
    ((102.42126, 155.28395), (107.13085, 155.28395)),  # Top
    ((103.02981, 155.99834), (106.41648, 155.99834)),  # Middle
    ((103.74419, 156.73917), (105.7021, 156.73917))    # Bottom
]

# Center vertical line
CENTER_LINE = ((106.7869, 143.45709), (106.7869, 147.5052))

# Canopy outline - approximated from SVG bezier path
CANOPY_OUTLINE = [
    (100.83, 143.74),   # Center bottom of canopy
    (99.72, 142.89),    # Left curve
    (99.51, 142.17),    # Left upper
    (99.65, 141.31),    # Left top bulge
    (100.08, 140.73),   # Upper left node area
    (101.48, 139.84),   # Upper left to center
    (102.85, 139.52),   # Upper center left
    (104.65, 139.34),   # Top center
    (106.30, 139.23),   # Upper center right
    (107.69, 139.78),   # Upper right
    (108.69, 141.06),   # Right side
    (108.85, 142.39)    # Right lower (stops here)
]

# Branch nodes (circles)
BRANCH_NODES = [
    (102.5271, 147.955),      # Bottom center
    (102.28898, 142.76917),   # Upper left
    (104.64377, 143.66875),   # Middle
    (106.7869, 142.92792),    # Right middle
    (108.18919, 145.25626)    # Far right
]

# Polylines (roots and branches) with their transforms
def apply_transform(points, a, e, f):
    """Apply SVG transform to points."""
    return [
        (a * x + e, a * y + f)
        for x, y in points
    ]

POLYLINES_WITH_TRANSFORM = [
    # Polyline 1 - right root
    apply_transform(
        [(99.8, 422.9), (99.8, 398.5), (110.5, 388.6), (110.5, 386.7)],
        0.26458333, 78.952727, 43.391667
    ),
    # Polyline 2 - left root
    apply_transform(
        [(95.3, 422.9), (95.3, 393.5), (88.2, 386.7), (88.2, 377.5)],
        0.26458333, 78.952727, 43.391667
    ),
    # Polyline 3 - left branch
    apply_transform(
        [(97.1, 381.1), (97.1, 384.3), (91.8, 390.1)],
        0.26458333, 78.952727, 43.391667
    ),
    # Polyline 4 - right branch
    apply_transform(
        [(89.1, 397.3), (89.1, 400.2), (95.3, 406.5)],
        0.26458333, 78.952727, 43.391667
    )
]


class SfLogo(Demo):
    """
    Bouncing Sequoia Fabrica tree logo with rainbow color cycling.

    The demo:
    - Displays a tree logo drawn with line segments and nodes
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

    def update(self):
        """Update logo position and animation state."""
        # Animate position (move every 8 frames)
        if self.frame_count % 8 == 0:
            self.x += self.sx
            if self.x > (self.canvas.width - SF_LOGO_WIDTH):
                self.x -= self.sx
                self.sy = 1
                self.y += self.sy
            if self.y > (self.canvas.height - SF_LOGO_HEIGHT):
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
        self.canvas.clear()

        # Get current color
        current_color = self.logo_color or self.palette[self.frame_count % 256]

        # Draw tree logo
        self._draw_tree_logo(self.x, self.y, current_color)

    def _svg_to_pixel(self, svg_x, svg_y):
        """Convert SVG coordinates to pixel coordinates."""
        x = int((svg_x - SVG_OFFSET_X) * SVG_SCALE_X + 0.5)
        y = int((svg_y - SVG_OFFSET_Y) * SVG_SCALE_Y + 0.5)
        return x, y

    def _screen_pos(self, px, py, offset_x, offset_y):
        """Apply offset and center positioning."""
        hw = self.canvas.width >> 1
        hh = self.canvas.height >> 1
        sx = offset_x + px + hw - (SF_LOGO_WIDTH // 2)
        sy = offset_y + py + hh - (SF_LOGO_HEIGHT // 2)
        return sx, sy

    def _draw_tree_logo(self, offset_x, offset_y, color):
        """Draw the tree logo at the given position."""
        # Draw canopy outline
        for i in range(len(CANOPY_OUTLINE) - 1):
            x0, y0 = self._svg_to_pixel(CANOPY_OUTLINE[i][0], CANOPY_OUTLINE[i][1])
            x1, y1 = self._svg_to_pixel(CANOPY_OUTLINE[i + 1][0], CANOPY_OUTLINE[i + 1][1])
            sx0, sy0 = self._screen_pos(x0, y0, offset_x, offset_y)
            sx1, sy1 = self._screen_pos(x1, y1, offset_x, offset_y)
            self._draw_line(sx0, sy0, sx1, sy1, color)

        # Draw trunk lines
        for line in TRUNK_LINES:
            x0, y0 = self._svg_to_pixel(line[0][0], line[0][1])
            x1, y1 = self._svg_to_pixel(line[1][0], line[1][1])
            sx0, sy0 = self._screen_pos(x0, y0, offset_x, offset_y)
            sx1, sy1 = self._screen_pos(x1, y1, offset_x, offset_y)
            self._draw_line(sx0, sy0, sx1, sy1, color)

        # Draw center vertical line
        cx0, cy0 = self._svg_to_pixel(CENTER_LINE[0][0], CENTER_LINE[0][1])
        cx1, cy1 = self._svg_to_pixel(CENTER_LINE[1][0], CENTER_LINE[1][1])
        scx0, scy0 = self._screen_pos(cx0, cy0, offset_x, offset_y)
        scx1, scy1 = self._screen_pos(cx1, cy1, offset_x, offset_y)
        self._draw_line(scx0, scy0, scx1, scy1, color)

        # Draw polylines (roots and branches)
        for polyline in POLYLINES_WITH_TRANSFORM:
            for i in range(len(polyline) - 1):
                x0, y0 = self._svg_to_pixel(polyline[i][0], polyline[i][1])
                x1, y1 = self._svg_to_pixel(polyline[i + 1][0], polyline[i + 1][1])
                sx0, sy0 = self._screen_pos(x0, y0, offset_x, offset_y)
                sx1, sy1 = self._screen_pos(x1, y1, offset_x, offset_y)
                self._draw_line(sx0, sy0, sx1, sy1, color)

        # Draw branch nodes (circles)
        node_radius = 1
        for node in BRANCH_NODES:
            px, py = self._svg_to_pixel(node[0], node[1])
            sx, sy = self._screen_pos(px, py, offset_x, offset_y)
            # Draw filled circle
            for dy in range(-node_radius, node_radius + 1):
                for dx in range(-node_radius, node_radius + 1):
                    if dx * dx + dy * dy <= node_radius * node_radius:
                        x = sx + dx
                        y = sy + dy
                        if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                            self.canvas.set_pixel(x, y, color)

    def _draw_line(self, x0, y0, x1, y1, color):
        """Draw line using Bresenham's algorithm."""
        x = x0
        y = y0
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)

            if x == x1 and y == y1:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

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
    run_demo(SfLogo)
