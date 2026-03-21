"""
Maze - Maze generation and solving animation
Ported from maze.cc by Carl Gorringe

Uses depth-first search with backtracking to generate a procedural maze.
The generation process is animated in real-time, showing how the algorithm
explores and backtracks through the maze grid.
"""

import random
from flaschen_taschen.demos import Demo
from flaschen_taschen.client.color import Color, ColorPalette
from flaschen_taschen.standard_options import StandardOptions


class Maze(Demo):
    """
    Maze generation using depth-first search algorithm.

    The display is divided into a 2x2 cell grid. Each cell is 2 pixels wide/tall.
    The algorithm generates one step per frame, showing the maze generation process.

    Color encoding:
    - BG (0): Background color
    - Maze (1): Foreground color (maze walls)
    - Visited (2): Cycling color (visited cells during generation)
    """

    def __init__(self, std_opts):
        super().__init__(std_opts)
        self.fg_color = Color(255, 255, 255)  # White by default
        self.visited_color = Color(0, 0, 0)
        self.bg_color = Color(0, 0, 0)
        self.use_fg_color = False
        self.use_visited_color = False
        self.use_bg_color = False

        # Parse demo-specific arguments
        args = std_opts.non_standard_args
        i = 0
        while i < len(args) and args[i].startswith('-'):
            arg = args[i]
            option = arg[1:]  # Remove leading '-'

            if option == 'c':
                i += 1
                if i < len(args):
                    color = self._parse_hex_color(args[i])
                    if color is not None:
                        self.fg_color = color
                        self.use_fg_color = True
            elif option == 'v':
                i += 1
                if i < len(args):
                    color = self._parse_hex_color(args[i])
                    if color is not None:
                        self.visited_color = color
                        self.use_visited_color = True
            elif option == 'b':
                i += 1
                if i < len(args):
                    color = self._parse_hex_color(args[i])
                    if color is not None:
                        self.bg_color = color
                        self.use_bg_color = True

            i += 1

    def setup(self):
        """Initialize maze generation state and palette."""
        super().setup()

        # Pixel buffer: 0=BG, 1=Maze, 2=Visited
        self.pixels = [0] * (self.canvas.width * self.canvas.height)

        # Create 256-color rainbow palette for visited color cycling
        self.palette = self._create_rainbow_palette()
        self.color_index = 0

        # Maze grid dimensions (each cell is 2x2 pixels)
        self.maze_width = self.canvas.width // 2
        self.maze_height = self.canvas.height // 2

        # Initialize cell stack with random starting position
        start_x = random.randint(0, self.maze_width - 1)
        start_y = random.randint(0, self.maze_height - 1)
        self.cell_stack = [(start_x, start_y)]

    def update(self):
        """Generate one step of the maze."""
        if not self.cell_stack:
            # Maze generation complete, keep animating
            return

        self._draw_maze_step()

    def draw(self):
        """Render the current maze state to canvas."""
        # Update visited color if cycling
        if not self.use_visited_color:
            self.visited_color = self.palette[self.color_index]
            self.color_index = (self.color_index + 1) % 256

        # Copy pixel buffer to canvas
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                pixel_idx = y * self.canvas.width + x
                pixel_value = self.pixels[pixel_idx]

                if pixel_value == 2:  # Visited
                    color = self.visited_color
                elif pixel_value == 1:  # Maze
                    color = self.fg_color
                else:  # BG
                    color = self.bg_color

                self.canvas.set_pixel(x, y, color)

    def _draw_maze_step(self):
        """Generate one step of the maze using depth-first search."""
        if not self.cell_stack:
            return

        pos_x, pos_y = self.cell_stack[-1]

        # Mark current position as maze
        cur_idx = pos_y * 2 * self.canvas.width + pos_x * 2
        self.pixels[cur_idx] = 1  # Maze

        # Find unvisited neighbors
        neighbors = []

        # Check up
        if pos_y > 0:
            temp_idx = (pos_y - 1) * 2 * self.canvas.width + pos_x * 2
            if self.pixels[temp_idx] == 0:  # Background
                neighbors.append((pos_x, pos_y - 1))

        # Check down
        if pos_y < self.maze_height - 1:
            temp_idx = (pos_y + 1) * 2 * self.canvas.width + pos_x * 2
            if self.pixels[temp_idx] == 0:
                neighbors.append((pos_x, pos_y + 1))

        # Check left
        if pos_x > 0:
            temp_idx = pos_y * 2 * self.canvas.width + (pos_x - 1) * 2
            if self.pixels[temp_idx] == 0:
                neighbors.append((pos_x - 1, pos_y))

        # Check right
        if pos_x < self.maze_width - 1:
            temp_idx = pos_y * 2 * self.canvas.width + (pos_x + 1) * 2
            if self.pixels[temp_idx] == 0:
                neighbors.append((pos_x + 1, pos_y))

        if neighbors:
            # Pick a random neighbor
            neighbor = random.choice(neighbors)

            # Remove wall between current and neighbor
            wall_x = pos_x + neighbor[0]
            wall_y = pos_y + neighbor[1]
            wall_idx = wall_y * self.canvas.width + wall_x
            self.pixels[wall_idx] = 1  # Maze

            # Push neighbor onto stack
            self.cell_stack.append(neighbor)
        else:
            # No unvisited neighbors - mark as visited and backtrack
            self.pixels[cur_idx] = 2  # Visited
            self.cell_stack.pop()

            # Draw wall to previous position if it exists
            if self.cell_stack:
                prev_x, prev_y = self.cell_stack[-1]
                wall_x = pos_x + prev_x
                wall_y = pos_y + prev_y
                wall_idx = wall_y * self.canvas.width + wall_x
                self.pixels[wall_idx] = 2  # Visited

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
        """Create a 256-color rainbow palette for visited color cycling."""
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
            Maze._add_gradient(palette, start, end, r1, g1, b1, r2, g2, b2)

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
    run_demo(Maze)
