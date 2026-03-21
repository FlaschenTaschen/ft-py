#!/usr/bin/env python3
"""
Life - Conway's Game of Life cellular automaton
Ported from life.cc by Carl Gorringe

Usage:
    python -m flaschen_taschen.demos.life [options]

Standard options:
    -h, --host HOST           Display hostname (default: localhost)
    -g, --geometry WxH[+X+Y]  Display geometry (default: 45x35)
    -l, --layer LAYER         Layer 0-15 (default: 0)
    -d, --delay MS            Frame delay in milliseconds (default: 0)
    -t, --timeout SECS        Timeout in seconds (default: 10)

Life-specific options:
    -r SECONDS     Respawn rate in seconds (default: 0 = no respawn)
    -c RRGGBB      Foreground color in hex (default: cycles through palette)
    -b RRGGBB      Background color in hex (default: black)
    -n DOTS        Initialize with 1/n random dots (default: 6)
"""

import time
import random
from flaschen_taschen.client.color import Color
from flaschen_taschen.standard_options import StandardOptions
from flaschen_taschen.demos import Demo


def parse_hex_color(hex_str):
    """Parse hex color string like 'ff0000' to Color"""
    try:
        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            return Color(r, g, b)
    except (ValueError, IndexError):
        pass
    return None


def create_rainbow_palette():
    """Create 256-color rainbow palette matching Swift implementation"""
    palette = []

    # Create 8 color gradients forming a rainbow
    def color_gradient(start, end, r1, g1, b1, r2, g2, b2):
        count = end - start
        for i in range(count + 1):
            k = i / count if count > 0 else 0
            r = int(r1 + (r2 - r1) * k)
            g = int(g1 + (g2 - g1) * k)
            b = int(b1 + (b2 - b1) * k)
            palette.append(Color(r, g, b))

    color_gradient(0, 31, 255, 0, 255, 0, 0, 255)          # magenta to blue
    color_gradient(32, 63, 0, 0, 255, 0, 255, 255)         # blue to cyan
    color_gradient(64, 95, 0, 255, 255, 0, 255, 0)         # cyan to green
    color_gradient(96, 127, 0, 255, 0, 127, 255, 0)        # green to light green
    color_gradient(128, 159, 127, 255, 0, 255, 255, 0)     # light green to yellow
    color_gradient(160, 191, 255, 255, 0, 255, 127, 0)     # yellow to orange
    color_gradient(192, 223, 255, 127, 0, 255, 0, 0)       # orange to red
    color_gradient(224, 255, 255, 0, 0, 255, 0, 255)       # red to magenta

    return palette


class Life:
    """Conway's Game of Life grid"""

    def __init__(self, width, height, density):
        """Initialize grid with random live cells

        Args:
            width: Grid width
            height: Grid height
            density: 1/density chance for a cell to be alive (e.g., 6 = 1/6 chance)
        """
        self.width = width
        self.height = height
        # Use bytes: 0 = dead, 1 = alive
        self.pixels = [0] * (width * height)

        # Initialize with random cells
        for i in range(width * height):
            # Random int in [0, density-1]: if 0, cell is alive
            self.pixels[i] = 1 if random.randint(0, density - 1) == 0 else 0

    def run_generation(self):
        """Execute one generation of Game of Life"""
        new_pixels = [0] * (self.width * self.height)

        for y in range(self.height):
            for x in range(self.width):
                # Count live neighbors with toroidal wrapping
                neighbor_count = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue

                        # Wrap coordinates around edges
                        ny = (y + dy) % self.height
                        nx = (x + dx) % self.width

                        if self.pixels[ny * self.width + nx]:
                            neighbor_count += 1

                idx = y * self.width + x
                is_alive = self.pixels[idx] != 0

                # Conway's Game of Life rules
                if is_alive:
                    # Live cell with 2-3 neighbors survives
                    new_pixels[idx] = 1 if neighbor_count in (2, 3) else 0
                else:
                    # Dead cell with exactly 3 neighbors becomes alive
                    new_pixels[idx] = 1 if neighbor_count == 3 else 0

        self.pixels = new_pixels

    def respawn(self, density):
        """Reinitialize grid with random live cells"""
        for i in range(self.width * self.height):
            self.pixels[i] = 1 if random.randint(0, density - 1) == 0 else 0


class LifeDemo(Demo):
    """Conway's Game of Life demo"""

    def __init__(self, std_opts):
        """Initialize with StandardOptions and parse Life-specific args

        Args:
            std_opts: StandardOptions with standard CLI arguments already parsed
        """
        super().__init__(std_opts)

        # Parse Life-specific options
        self.respawn_rate = 0.0
        self.has_custom_fg_color = False
        self.fg_color = Color(255, 255, 255)
        self.has_custom_bg_color = False
        self.bg_color = Color(0, 0, 0)
        self.num_dots = 6

        args = std_opts.non_standard_args
        i = 0
        while i < len(args) and args[i].startswith("-"):
            arg = args[i]
            option = arg[1:]

            if option == "r":
                i += 1
                if i < len(args):
                    try:
                        self.respawn_rate = float(args[i])
                    except ValueError:
                        pass
            elif option == "c":
                i += 1
                if i < len(args):
                    color = parse_hex_color(args[i])
                    if color:
                        self.fg_color = color
                        self.has_custom_fg_color = True
            elif option == "b":
                i += 1
                if i < len(args):
                    color = parse_hex_color(args[i])
                    if color:
                        self.bg_color = color
                        self.has_custom_bg_color = True
            elif option == "n":
                i += 1
                if i < len(args):
                    try:
                        self.num_dots = int(args[i])
                    except ValueError:
                        pass
            i += 1

        self.game = None
        self.palette = None
        self.palette_index = 0
        self.last_respawn_time = time.time()

    def setup(self):
        """Initialize game and palette"""
        super().setup()
        assert self.canvas is not None

        self.game = Life(self.canvas.width, self.canvas.height, self.num_dots)
        self.palette = create_rainbow_palette()
        self.last_respawn_time = time.time()

    def update(self):
        """Run one generation and check for respawn"""
        self.game.run_generation()

        # Check for respawn
        if self.respawn_rate > 0:
            now = time.time()
            if now - self.last_respawn_time > self.respawn_rate:
                self.last_respawn_time = now
                self.game.respawn(self.num_dots)

    def draw(self):
        """Render game state to canvas"""
        # Determine colors for this frame
        if self.has_custom_fg_color:
            display_fg_color = self.fg_color
        else:
            display_fg_color = self.palette[self.palette_index]

        display_bg_color = self.bg_color

        # Render to canvas
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                is_alive = self.game.pixels[y * self.canvas.width + x] != 0
                color = display_fg_color if is_alive else display_bg_color
                self.canvas.set_pixel(x, y, color)

        # Advance palette color for next frame
        self.palette_index = (self.palette_index + 1) % 256

    def cleanup(self):
        """Cleanup resources"""
        self.game = None
        self.palette = None


if __name__ == "__main__":
    from flaschen_taschen.demos import run_demo
    run_demo(LifeDemo)
