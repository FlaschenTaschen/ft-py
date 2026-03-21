"""
Lines - Random line drawing animation
Ported from lines.cc by Carl Gorringe

Draws randomly moving lines that bounce off canvas edges with smooth color transitions.
Each line's endpoints move independently with random velocity, and colors transition
smoothly between random target colors.
"""

import random
from flaschen_taschen.demos import Demo
from flaschen_taschen.client.color import Color
from flaschen_taschen.standard_options import StandardOptions


class Line:
    """Represents a line with two endpoints."""
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        return f"Line({self.x1},{self.y1})-({self.x2},{self.y2})"


class ColorState:
    """Manages color animation with smooth transitions."""
    def __init__(self):
        self.count = 0
        self.old_r = 0
        self.old_g = 0
        self.old_b = 0
        self.new_r = 0
        self.new_g = 0
        self.new_b = 0
        self.skp_r = 0
        self.skp_g = 0
        self.skp_b = 0
        self.cur_r = 0
        self.cur_g = 0
        self.cur_b = 0

    def reset(self):
        """Reset color state."""
        self.count = 0


class LineState:
    """Manages line animation with circular buffer."""
    def __init__(self, num_lines=6):
        self.lines_array = [Line() for _ in range(num_lines)]
        self.lines_idx = 0
        self.line_skip = Line()


class Lines(Demo):
    """
    Lines demo - draws randomly moving lines with smooth color transitions.

    The animation:
    - Maintains a circular buffer of 6 lines
    - Each frame: erase old line, compute new endpoints, draw with new color
    - Endpoints move with random velocity and bounce off edges
    - Colors transition smoothly over 16 frames
    - Can draw 1, 2, or 4 lines with mirror/reflection symmetry
    """

    def __init__(self, std_opts):
        super().__init__(std_opts)
        self.draw_num = 1

        # Parse draw mode argument (one, two, or four)
        args = std_opts.non_standard_args
        if args:
            mode = args[0].lower()
            if mode.startswith('one'):
                self.draw_num = 1
            elif mode.startswith('two'):
                self.draw_num = 2
            elif mode.startswith('four'):
                self.draw_num = 4
            else:
                self.draw_num = 1

    def setup(self):
        """Initialize line and color state."""
        super().setup()

        self.color_state = ColorState()
        self.line_state = LineState(num_lines=6)
        self.transparent = Color(0, 0, 0)

        # Initialize first color and line
        self.current_color = self._next_color(reset=True)
        self.current_line = self._next_line(reset=True)

    def update(self):
        """Update line positions and colors."""
        # Get next color and line
        self.current_color = self._next_color(reset=False)
        self.current_line = self._next_line(reset=False)

    def draw(self):
        """Draw the lines to canvas."""
        # Erase previous line by drawing with transparent color
        self._draw_all_lines(self._last_line(), self.transparent)

        # Draw new line with current color
        self._draw_all_lines(self.current_line, self.current_color)

    def _next_color(self, reset=False):
        """Generate next color with smooth transitions."""
        if reset:
            self.color_state.reset()

        self.color_state.count -= 1
        if self.color_state.count < 0:
            self.color_state.count = 15
            self.color_state.old_r = self.color_state.new_r
            self.color_state.old_g = self.color_state.new_g
            self.color_state.old_b = self.color_state.new_b

            # Pick new random color (not black)
            while True:
                self.color_state.new_r = random.randint(0, 1) * 255
                self.color_state.new_g = random.randint(0, 1) * 255
                self.color_state.new_b = random.randint(0, 1) * 255
                if not (self.color_state.new_r == 0 and self.color_state.new_g == 0 and self.color_state.new_b == 0):
                    break

            # Calculate step size for smooth transition
            self.color_state.skp_r = 0 if self.color_state.new_r == self.color_state.old_r else (
                16 if self.color_state.new_r > self.color_state.old_r else -16)
            self.color_state.skp_g = 0 if self.color_state.new_g == self.color_state.old_g else (
                16 if self.color_state.new_g > self.color_state.old_g else -16)
            self.color_state.skp_b = 0 if self.color_state.new_b == self.color_state.old_b else (
                16 if self.color_state.new_b > self.color_state.old_b else -16)

            self.color_state.cur_r = self.color_state.old_r
            self.color_state.cur_g = self.color_state.old_g
            self.color_state.cur_b = self.color_state.old_b

        # Interpolate toward new color
        self.color_state.cur_r += self.color_state.skp_r
        self.color_state.cur_g += self.color_state.skp_g
        self.color_state.cur_b += self.color_state.skp_b

        # Convert from 0-256 range to 0-255
        r = int(self.color_state.cur_r / 256.0 * 255.0)
        g = int(self.color_state.cur_g / 256.0 * 255.0)
        b = int(self.color_state.cur_b / 256.0 * 255.0)

        return Color(r, g, b)

    def _next_line(self, reset=False):
        """Generate next line endpoint positions."""
        old_idx = self.line_state.lines_idx
        self.line_state.lines_idx += 1
        if self.line_state.lines_idx >= len(self.line_state.lines_array):
            self.line_state.lines_idx = 0

        if reset:
            # Initialize with random endpoints
            self.line_state.lines_array[self.line_state.lines_idx] = Line(
                x1=random.randint(1, self.canvas.width - 2),
                y1=random.randint(1, self.canvas.height - 2),
                x2=random.randint(1, self.canvas.width - 2),
                y2=random.randint(1, self.canvas.height - 2)
            )

            # Initialize random skip velocities
            self.line_state.line_skip = Line(
                x1=random.randint(1, 3) if random.randint(0, 1) else -random.randint(1, 3),
                y1=random.randint(1, 3) if random.randint(0, 1) else -random.randint(1, 3),
                x2=random.randint(1, 3) if random.randint(0, 1) else -random.randint(1, 3),
                y2=random.randint(1, 3) if random.randint(0, 1) else -random.randint(1, 3)
            )
        else:
            # Move endpoints by skip velocity
            new_line = Line(
                x1=self.line_state.lines_array[old_idx].x1 + self.line_state.line_skip.x1,
                y1=self.line_state.lines_array[old_idx].y1 + self.line_state.line_skip.y1,
                x2=self.line_state.lines_array[old_idx].x2 + self.line_state.line_skip.x2,
                y2=self.line_state.lines_array[old_idx].y2 + self.line_state.line_skip.y2
            )

            # Bounce off edges
            if new_line.x1 <= 0:
                self.line_state.line_skip.x1 = random.randint(1, 3)
            if new_line.x1 >= self.canvas.width:
                self.line_state.line_skip.x1 = -random.randint(1, 3)
            if new_line.y1 <= 0:
                self.line_state.line_skip.y1 = random.randint(1, 3)
            if new_line.y1 >= self.canvas.height:
                self.line_state.line_skip.y1 = -random.randint(1, 3)

            if new_line.x2 <= 0:
                self.line_state.line_skip.x2 = random.randint(1, 3)
            if new_line.x2 >= self.canvas.width:
                self.line_state.line_skip.x2 = -random.randint(1, 3)
            if new_line.y2 <= 0:
                self.line_state.line_skip.y2 = random.randint(1, 3)
            if new_line.y2 >= self.canvas.height:
                self.line_state.line_skip.y2 = -random.randint(1, 3)

            self.line_state.lines_array[self.line_state.lines_idx] = new_line

        return self.line_state.lines_array[self.line_state.lines_idx]

    def _last_line(self):
        """Get the previously drawn line (circular buffer)."""
        last_idx = self.line_state.lines_idx + 1
        if last_idx >= len(self.line_state.lines_array):
            last_idx = 0
        return self.line_state.lines_array[last_idx]

    def _draw_all_lines(self, line, color):
        """Draw line(s) with optional mirror symmetry."""
        self._draw_line(line.x1, line.y1, line.x2, line.y2, color)

        if self.draw_num >= 2:
            # Horizontal flip
            self._draw_line(
                self.canvas.width - line.x1, self.canvas.height - line.y1,
                self.canvas.width - line.x2, self.canvas.height - line.y2,
                color
            )

        if self.draw_num == 4:
            # Two additional reflections
            self._draw_line(
                self.canvas.width - line.x1, line.y1,
                self.canvas.width - line.x2, line.y2,
                color
            )
            self._draw_line(
                line.x1, self.canvas.height - line.y1,
                line.x2, self.canvas.height - line.y2,
                color
            )

    def _draw_line(self, x1, y1, x2, y2, color):
        """Draw a line using Bresenham's line algorithm."""
        x = x1
        y = y1
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            # Draw pixel if within bounds
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)

            # Check if we've reached the end
            if x == x2 and y == y2:
                break

            # Bresenham step
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy


if __name__ == '__main__':
    from flaschen_taschen.demos import run_demo
    run_demo(Lines)
