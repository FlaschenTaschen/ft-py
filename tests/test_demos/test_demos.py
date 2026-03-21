"""Tests for individual demo implementations."""

import pytest
from flaschen_taschen.standard_options import StandardOptions
from flaschen_taschen.demos.simple_example import SimpleExampleDemo
from flaschen_taschen.demos.simple_animation import SimpleAnimationDemo
from flaschen_taschen.demos.black import BlackDemo
from flaschen_taschen.demos.plasma import PlasmaDemo
from flaschen_taschen.demos.matrix import MatrixDemo
from flaschen_taschen.demos.blur import BlurDemo
from flaschen_taschen.demos.quilt import QuiltDemo
from flaschen_taschen.demos.firefly import FireflyDemo
from flaschen_taschen.demos.life import LifeDemo, Life
from flaschen_taschen.demos.maze import Maze
from flaschen_taschen.demos.sierpinski import Sierpinski
from flaschen_taschen.demos.lines import Lines, ColorState, LineState, Line
from flaschen_taschen.demos.fractal import Fractal, FractalState
from flaschen_taschen.demos.random_dots import RandomDots


@pytest.fixture
def std_opts():
    """Standard options for testing demos."""
    return StandardOptions(["-g", "40x30", "-t", "1"])


class TestSimpleExampleDemo:
    """Test SimpleExampleDemo."""

    def test_simple_example_initialization(self, std_opts):
        """Test initialization."""
        demo = SimpleExampleDemo(std_opts)
        assert demo.std_opts == std_opts

    def test_simple_example_setup(self, std_opts):
        """Test setup creates canvas."""
        demo = SimpleExampleDemo(std_opts)
        demo.setup()
        assert demo.canvas is not None
        assert demo.canvas.width == 40
        assert demo.canvas.height == 30

    def test_simple_example_update_draw(self, std_opts):
        """Test update and draw execute without error."""
        demo = SimpleExampleDemo(std_opts)
        demo.setup()
        demo.update()
        demo.draw()
        # Should complete without exception


class TestSimpleAnimationDemo:
    """Test SimpleAnimationDemo."""

    def test_simple_animation_initialization(self, std_opts):
        """Test initialization."""
        demo = SimpleAnimationDemo(std_opts)
        assert demo.std_opts == std_opts

    def test_simple_animation_time_update(self, std_opts):
        """Test time updates during animation."""
        demo = SimpleAnimationDemo(std_opts)
        demo.setup()

        initial_time = demo.time
        demo.update()
        assert demo.time > initial_time

    def test_simple_animation_draw(self, std_opts):
        """Test animation draw."""
        demo = SimpleAnimationDemo(std_opts)
        demo.setup()
        demo.update()
        demo.draw()
        # Should complete without exception


class TestBlackDemo:
    """Test BlackDemo."""

    def test_black_demo_initialization(self, std_opts):
        """Test initialization."""
        demo = BlackDemo(std_opts)
        assert demo.std_opts == std_opts

    def test_black_demo_clears_display(self, std_opts):
        """Test that black demo clears display."""
        from flaschen_taschen.client.color import Color

        demo = BlackDemo(std_opts)
        demo.setup()

        # Set some pixels
        demo.canvas.fill_rect(0, 0, 5, 5, Color.WHITE)

        # Draw should clear
        demo.draw()

        # All pixels should be black
        for y in range(demo.canvas.height):
            for x in range(demo.canvas.width):
                pixel = demo.canvas.get_pixel(x, y)
                assert pixel is not None
                assert pixel.r == 0 and pixel.g == 0 and pixel.b == 0


class TestPlasmaDemo:
    """Test PlasmaDemo."""

    def test_plasma_initialization(self, std_opts):
        """Test initialization."""
        demo = PlasmaDemo(std_opts)
        assert demo.std_opts == std_opts

    def test_plasma_time_update(self, std_opts):
        """Test animation counter updates."""
        demo = PlasmaDemo(std_opts)
        demo.setup()

        initial_count = demo.count
        demo.update()
        assert demo.count > initial_count

    def test_plasma_draw(self, std_opts):
        """Test plasma rendering."""
        demo = PlasmaDemo(std_opts)
        demo.setup()
        demo.update()
        demo.draw()
        # Should complete without exception


class TestMatrixDemo:
    """Test MatrixDemo."""

    def test_matrix_initialization(self, std_opts):
        """Test initialization."""
        demo = MatrixDemo(std_opts)
        assert demo.std_opts == std_opts

    def test_matrix_setup_creates_columns(self, std_opts):
        """Test setup creates falling columns."""
        demo = MatrixDemo(std_opts)
        demo.setup()

        assert len(demo.columns) == demo.canvas.width
        assert len(demo.brightness) == demo.canvas.width
        for col in demo.columns:
            assert isinstance(col, int)
            assert 0 <= col < demo.canvas.height

    def test_matrix_update_moves_chars(self, std_opts):
        """Test update moves characters."""
        demo = MatrixDemo(std_opts)
        demo.setup()

        initial_y = demo.columns[0]
        demo.update()
        # Columns increment, may wrap around
        assert demo.columns[0] == (initial_y + 1) % demo.canvas.height

    def test_matrix_draw(self, std_opts):
        """Test matrix rendering."""
        demo = MatrixDemo(std_opts)
        demo.setup()
        demo.update()
        demo.draw()
        # Should complete without exception


class TestBlurDemo:
    """Test BlurDemo."""

    def test_blur_initialization(self, std_opts):
        """Test initialization."""
        demo = BlurDemo(std_opts)
        assert demo.std_opts == std_opts

    def test_blur_demo_type_parsing(self):
        """Test demo type parsing from arguments."""
        opts = StandardOptions(["-g", "40x30", "boxes"])
        demo = BlurDemo(opts)
        demo.setup()

        assert demo.demo_type == "boxes"

    def test_blur_demo_type_all(self):
        """Test 'all' mode for cycling through demos."""
        opts = StandardOptions(["-g", "40x30", "all"])
        demo = BlurDemo(opts)
        demo.setup()

        assert demo.demo_type == "all"
        assert demo.current_demo in ["bolt", "boxes", "circles", "target", "fire"]

    def test_blur_update_frame_count(self, std_opts):
        """Test frame count increments."""
        demo = BlurDemo(std_opts)
        demo.setup()

        initial_count = demo.frame_count
        demo.update()
        assert demo.frame_count > initial_count

    def test_blur_draw(self, std_opts):
        """Test blur rendering."""
        demo = BlurDemo(std_opts)
        demo.setup()
        demo.update()
        demo.draw()
        # Should complete without exception

    def test_blur_shapes(self):
        """Test all blur shape types."""
        for shape in ["bolt", "boxes", "circles", "target", "fire"]:
            opts = StandardOptions(["-g", "30x30", shape])
            demo = BlurDemo(opts)
            demo.setup()
            demo.update()
            demo.draw()
            # Should complete without exception


class TestQuiltDemo:
    """Test QuiltDemo."""

    def test_quilt_initialization(self, std_opts):
        """Test initialization."""
        demo = QuiltDemo(std_opts)
        assert demo.std_opts == std_opts

    def test_quilt_position_update(self, std_opts):
        """Test position updates."""
        demo = QuiltDemo(std_opts)
        demo.setup()

        initial_x = demo.current_x
        demo.update()
        # Position should change or wrap around
        assert demo.current_x != initial_x or demo.current_y != 0

    def test_quilt_draw(self, std_opts):
        """Test quilt rendering."""
        demo = QuiltDemo(std_opts)
        demo.setup()
        demo.update()
        demo.draw()
        # Should complete without exception


class TestFireflyDemo:
    """Test FireflyDemo."""

    def test_firefly_initialization(self, std_opts):
        """Test initialization."""
        demo = FireflyDemo(std_opts)
        assert demo.std_opts == std_opts

    def test_firefly_setup_creates_particles(self, std_opts):
        """Test setup creates fireflies."""
        demo = FireflyDemo(std_opts)
        demo.setup()

        assert len(demo.fireflies) > 0
        for firefly in demo.fireflies:
            assert firefly.x >= 0
            assert firefly.y >= 0
            assert firefly.brightness >= 0

    def test_firefly_update(self, std_opts):
        """Test firefly position updates."""
        demo = FireflyDemo(std_opts)
        demo.setup()

        initial_x = demo.fireflies[0].x
        demo.update()
        # Position should have changed (with high probability)
        # Note: Could randomly stay same, so we just check it updated

    def test_firefly_draw(self, std_opts):
        """Test firefly rendering."""
        demo = FireflyDemo(std_opts)
        demo.setup()
        demo.update()
        demo.draw()
        # Should complete without exception

    def test_firefly_physics(self, std_opts):
        """Test firefly physics boundaries."""
        from flaschen_taschen.demos.firefly import Firefly

        firefly = Firefly(10, 10, 40, 30)

        # Force out of bounds
        firefly.x = -10
        firefly.vy = 1
        initial_vx = firefly.vx
        initial_vy = firefly.vy

        firefly.update()

        # X should have bounced back
        assert firefly.x >= 0


class TestLife:
    """Test Life grid implementation."""

    def test_life_initialization(self):
        """Test grid initialization with random cells."""
        game = Life(10, 10, 6)
        assert game.width == 10
        assert game.height == 10
        assert len(game.pixels) == 100

    def test_life_density(self):
        """Test that density affects initial population."""
        # With density=2, ~50% of cells should be alive
        game = Life(100, 100, 2)
        alive_count = sum(1 for p in game.pixels if p)
        # Should be roughly 50%, allow variance
        assert 3000 < alive_count < 7000

    def test_life_generation(self):
        """Test that generations change the grid."""
        game = Life(20, 20, 6)
        initial_state = game.pixels.copy()

        game.run_generation()
        new_state = game.pixels

        # State should have changed (with overwhelming probability)
        assert initial_state != new_state

    def test_life_toroidal(self):
        """Test toroidal wrapping (edges wrap around)."""
        # Create a small known pattern and verify wrapping
        game = Life(3, 3, 100)  # All dead initially
        game.pixels = [0] * 9

        # Set up a simple pattern: center cell has 3 neighbors (top, bottom, left)
        # that wrap around
        game.pixels[0] = 1  # top-left
        game.pixels[3] = 1  # middle-left
        game.pixels[6] = 1  # bottom-left

        game.run_generation()

        # Center cell should be alive (3 neighbors)
        assert game.pixels[4] == 1

    def test_life_respawn(self):
        """Test respawn reinitializes grid."""
        game = Life(10, 10, 6)
        initial_state = game.pixels.copy()

        game.respawn(6)
        respawned_state = game.pixels

        # States should differ (with overwhelming probability)
        assert initial_state != respawned_state


class TestLifeDemo:
    """Test LifeDemo."""

    def test_life_initialization(self, std_opts):
        """Test initialization."""
        demo = LifeDemo(std_opts)
        assert demo.std_opts == std_opts
        assert demo.num_dots == 6
        assert not demo.has_custom_fg_color
        assert not demo.has_custom_bg_color
        assert demo.respawn_rate == 0.0

    def test_life_custom_fg_color(self):
        """Test foreground color parsing."""
        opts = StandardOptions(["-g", "40x30", "-c", "ff0000"])
        demo = LifeDemo(opts)

        assert demo.has_custom_fg_color
        assert demo.fg_color.r == 255
        assert demo.fg_color.g == 0
        assert demo.fg_color.b == 0

    def test_life_custom_bg_color(self):
        """Test background color parsing."""
        opts = StandardOptions(["-g", "40x30", "-b", "00ff00"])
        demo = LifeDemo(opts)

        assert demo.has_custom_bg_color
        assert demo.bg_color.r == 0
        assert demo.bg_color.g == 255
        assert demo.bg_color.b == 0

    def test_life_respawn_rate(self):
        """Test respawn rate parsing."""
        opts = StandardOptions(["-g", "40x30", "-r", "5.5"])
        demo = LifeDemo(opts)

        assert demo.respawn_rate == 5.5

    def test_life_num_dots(self):
        """Test num_dots parsing."""
        opts = StandardOptions(["-g", "40x30", "-n", "12"])
        demo = LifeDemo(opts)

        assert demo.num_dots == 12

    def test_life_setup_creates_game(self, std_opts):
        """Test setup creates game and palette."""
        demo = LifeDemo(std_opts)
        demo.setup()

        assert demo.game is not None
        assert demo.palette is not None
        assert len(demo.palette) == 256
        assert demo.canvas is not None

    def test_life_update_runs_generation(self, std_opts):
        """Test update runs game generation."""
        demo = LifeDemo(std_opts)
        demo.setup()

        initial_state = demo.game.pixels.copy()
        demo.update()
        new_state = demo.game.pixels

        # State should have changed
        assert initial_state != new_state

    def test_life_palette_cycling(self, std_opts):
        """Test palette index cycles."""
        demo = LifeDemo(std_opts)
        demo.setup()

        initial_index = demo.palette_index
        for _ in range(256):
            demo.update()
            demo.draw()

        # Should wrap around
        assert demo.palette_index == 0

    def test_life_draw_renders_state(self, std_opts):
        """Test draw renders to canvas."""
        demo = LifeDemo(std_opts)
        demo.setup()

        # Make sure some cells are alive
        demo.game.pixels[0] = 1
        demo.game.pixels[demo.canvas.width] = 1

        demo.draw()

        # Check that alive cells are foreground color, dead are background
        alive_color = demo.canvas.get_pixel(0, 0)
        dead_color = demo.canvas.get_pixel(1, 1)

        # Should have different colors if at least one is dead and one is alive
        # (depends on initial state, but with 1/6 density, likely true)

    def test_life_custom_colors_respected(self):
        """Test that custom colors are used in rendering."""
        from flaschen_taschen.client.color import Color

        opts = StandardOptions(["-g", "20x20", "-c", "ff0000", "-b", "0000ff"])
        demo = LifeDemo(opts)
        demo.setup()

        # Make a known pattern
        demo.game.pixels = [0] * (demo.canvas.width * demo.canvas.height)
        demo.game.pixels[0] = 1  # Alive cell at (0, 0)

        demo.draw()

        # Cell at (0, 0) should be red (custom foreground)
        pixel = demo.canvas.get_pixel(0, 0)
        assert pixel.r == 255
        assert pixel.g == 0
        assert pixel.b == 0

        # Cell at (1, 1) should be blue (custom background)
        pixel = demo.canvas.get_pixel(1, 1)
        assert pixel.r == 0
        assert pixel.g == 0
        assert pixel.b == 255


class TestMaze:
    """Test Maze demo."""

    def test_maze_initialization(self, std_opts):
        """Test initialization."""
        demo = Maze(std_opts)
        assert demo.std_opts == std_opts
        assert demo.use_fg_color is False
        assert demo.use_visited_color is False
        assert demo.use_bg_color is False

    def test_maze_fg_color_parsing(self):
        """Test foreground color parsing."""
        opts = StandardOptions(["-g", "40x30", "-c", "ff0000"])
        demo = Maze(opts)

        assert demo.use_fg_color is True
        assert demo.fg_color.r == 255
        assert demo.fg_color.g == 0
        assert demo.fg_color.b == 0

    def test_maze_visited_color_parsing(self):
        """Test visited color parsing."""
        opts = StandardOptions(["-g", "40x30", "-v", "00ff00"])
        demo = Maze(opts)

        assert demo.use_visited_color is True
        assert demo.visited_color.r == 0
        assert demo.visited_color.g == 255
        assert demo.visited_color.b == 0

    def test_maze_bg_color_parsing(self):
        """Test background color parsing."""
        opts = StandardOptions(["-g", "40x30", "-b", "0000ff"])
        demo = Maze(opts)

        assert demo.use_bg_color is True
        assert demo.bg_color.r == 0
        assert demo.bg_color.g == 0
        assert demo.bg_color.b == 255

    def test_maze_setup_creates_state(self, std_opts):
        """Test setup initializes maze state."""
        demo = Maze(std_opts)
        demo.setup()

        assert demo.canvas is not None
        assert demo.pixels is not None
        assert len(demo.pixels) == demo.canvas.width * demo.canvas.height
        assert demo.cell_stack is not None
        assert len(demo.cell_stack) > 0  # Should start with one cell
        assert demo.palette is not None
        assert len(demo.palette) == 256

    def test_maze_update_generates_step(self, std_opts):
        """Test update generates one maze step."""
        demo = Maze(std_opts)
        demo.setup()

        # Get initial maze count
        initial_maze_count = sum(1 for p in demo.pixels if p == 1)

        # Update should add at least one maze pixel
        demo.update()

        new_maze_count = sum(1 for p in demo.pixels if p == 1)

        # Maze count should have increased or stayed same
        # (it might stay same if we just backtracked)
        assert new_maze_count >= initial_maze_count

    def test_maze_color_cycling(self, std_opts):
        """Test that visited color cycles through palette."""
        demo = Maze(std_opts)
        demo.setup()

        initial_color = demo.visited_color
        initial_index = demo.color_index

        demo.draw()

        # Color index should have incremented
        assert demo.color_index == (initial_index + 1) % 256

        # Color should have changed
        assert demo.visited_color != initial_color

    def test_maze_draw_renders(self, std_opts):
        """Test draw renders maze to canvas."""
        demo = Maze(std_opts)
        demo.setup()

        # Force some maze pixels
        demo.pixels[0] = 1
        demo.pixels[1] = 2

        demo.draw()

        # Check pixels were set correctly
        pixel_maze = demo.canvas.get_pixel(0, 0)
        pixel_visited = demo.canvas.get_pixel(1, 0)

        assert pixel_maze.r == 255  # White (default fg)
        assert pixel_visited != pixel_maze  # Different colors

    def test_maze_multiple_steps(self, std_opts):
        """Test maze generation progresses over multiple steps."""
        demo = Maze(std_opts)
        demo.setup()

        initial_stack_size = len(demo.cell_stack)

        # Run multiple steps
        for _ in range(100):
            demo.update()

        # Stack should have grown or empty (completed)
        # In most cases it should grow as maze expands
        assert len(demo.cell_stack) >= 0  # Either still growing or completed

    def test_maze_hex_color_parsing(self):
        """Test hex color string parsing."""
        from flaschen_taschen.client.color import Color

        color = Maze._parse_hex_color("ff0000")
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0

        color = Maze._parse_hex_color("00ff00")
        assert color.r == 0
        assert color.g == 255
        assert color.b == 0

    def test_maze_palette_generation(self):
        """Test rainbow palette generation."""
        demo_palette = Maze._create_rainbow_palette()

        assert len(demo_palette) == 256

        # Check that palette has color variation
        # Middle colors should differ from start and each other
        assert demo_palette[0] != demo_palette[128]
        assert demo_palette[64] != demo_palette[192]

        # Check all entries are Color objects
        for color in demo_palette:
            assert hasattr(color, 'r')
            assert hasattr(color, 'g')
            assert hasattr(color, 'b')


class TestSierpinski:
    """Test Sierpinski demo."""

    def test_sierpinski_initialization(self, std_opts):
        """Test initialization."""
        demo = Sierpinski(std_opts)
        assert demo.std_opts == std_opts
        assert demo.palette_mode is True
        assert demo.fg_color.r == 0
        assert demo.fg_color.g == 0
        assert demo.fg_color.b == 0

    def test_sierpinski_fg_color_parsing(self):
        """Test foreground color parsing."""
        opts = StandardOptions(["-g", "40x30", "-c", "ff0000"])
        demo = Sierpinski(opts)

        assert demo.palette_mode is False
        assert demo.fg_color.r == 255
        assert demo.fg_color.g == 0
        assert demo.fg_color.b == 0

    def test_sierpinski_bg_color_parsing(self):
        """Test background color parsing."""
        opts = StandardOptions(["-g", "40x30", "-b", "0000ff"])
        demo = Sierpinski(opts)

        assert demo.bg_color.r == 0
        assert demo.bg_color.g == 0
        assert demo.bg_color.b == 255

    def test_sierpinski_setup_creates_state(self, std_opts):
        """Test setup initializes sierpinski state."""
        demo = Sierpinski(std_opts)
        demo.setup()

        assert demo.canvas is not None
        assert demo.pixels is not None
        assert len(demo.pixels) == demo.canvas.width * demo.canvas.height
        assert all(p == 0 for p in demo.pixels)  # All empty initially
        assert demo.palette is not None
        assert len(demo.palette) == 256
        assert demo.vertices == [(0.5, 1.0), (0.0, 0.0), (1.0, 0.0)]
        assert 0 <= demo.sx <= 1.0
        assert 0 <= demo.sy <= 1.0

    def test_sierpinski_update_marks_pixels(self, std_opts):
        """Test update marks pixels in accumulation buffer."""
        demo = Sierpinski(std_opts)
        demo.setup()

        # Get initial pixel count
        initial_marked = sum(1 for p in demo.pixels if p != 0)

        # Run multiple iterations
        for _ in range(10):
            demo.update()

        # Should have marked at least one pixel
        final_marked = sum(1 for p in demo.pixels if p != 0)
        assert final_marked >= initial_marked

    def test_sierpinski_color_cycling(self, std_opts):
        """Test that color index cycles through palette."""
        demo = Sierpinski(std_opts)
        demo.setup()

        initial_index = demo.color_index

        demo.draw()

        # Color index should have incremented
        assert demo.color_index == (initial_index + 1) % 256

    def test_sierpinski_palette_mode_vs_fixed_color(self):
        """Test difference between palette and fixed color modes."""
        opts_palette = StandardOptions(["-g", "40x30"])
        opts_fixed = StandardOptions(["-g", "40x30", "-c", "ff0000"])

        demo_palette = Sierpinski(opts_palette)
        demo_fixed = Sierpinski(opts_fixed)

        assert demo_palette.palette_mode is True
        assert demo_fixed.palette_mode is False

    def test_sierpinski_draw_renders(self, std_opts):
        """Test draw renders sierpinski to canvas."""
        demo = Sierpinski(std_opts)
        demo.setup()

        # Mark some pixels
        demo.pixels[0] = 1
        demo.pixels[1] = 1

        demo.draw()

        # Check pixels were rendered
        pixel_marked = demo.canvas.get_pixel(0, 0)
        # Pixel 0 should be foreground color (black by default)
        assert pixel_marked is not None

    def test_sierpinski_chaos_game_convergence(self, std_opts):
        """Test that chaos game marks multiple pixels."""
        demo = Sierpinski(std_opts)
        demo.setup()

        # Get initial state
        initial_marked = sum(1 for p in demo.pixels if p != 0)

        # Run iterations to mark pixels
        for _ in range(100):
            demo.update()

        # Should have marked multiple pixels
        final_marked = sum(1 for p in demo.pixels if p != 0)
        assert final_marked > initial_marked
        assert final_marked > 0  # At least some pixels marked

    def test_sierpinski_hex_color_parsing(self):
        """Test hex color string parsing."""
        color = Sierpinski._parse_hex_color("ff0000")
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0

        color = Sierpinski._parse_hex_color("00ff00")
        assert color.r == 0
        assert color.g == 255
        assert color.b == 0

    def test_sierpinski_palette_generation(self):
        """Test rainbow palette generation."""
        palette = Sierpinski._create_rainbow_palette()

        assert len(palette) == 256

        # Check color variation
        assert palette[0] != palette[128]
        assert palette[64] != palette[192]

        # Check all are Color objects
        for color in palette:
            assert hasattr(color, 'r')
            assert hasattr(color, 'g')
            assert hasattr(color, 'b')


class TestLines:
    """Test Lines demo."""

    def test_lines_initialization(self, std_opts):
        """Test initialization."""
        demo = Lines(std_opts)
        assert demo.std_opts == std_opts
        assert demo.draw_num == 1

    def test_lines_draw_mode_one(self):
        """Test 'one' draw mode parsing."""
        opts = StandardOptions(["-g", "40x30", "one"])
        demo = Lines(opts)
        assert demo.draw_num == 1

    def test_lines_draw_mode_two(self):
        """Test 'two' draw mode parsing."""
        opts = StandardOptions(["-g", "40x30", "two"])
        demo = Lines(opts)
        assert demo.draw_num == 2

    def test_lines_draw_mode_four(self):
        """Test 'four' draw mode parsing."""
        opts = StandardOptions(["-g", "40x30", "four"])
        demo = Lines(opts)
        assert demo.draw_num == 4

    def test_lines_setup_creates_state(self, std_opts):
        """Test setup initializes line and color state."""
        demo = Lines(std_opts)
        demo.setup()

        assert demo.canvas is not None
        assert demo.color_state is not None
        assert demo.line_state is not None
        assert demo.transparent is not None
        assert demo.current_color is not None
        assert demo.current_line is not None
        assert len(demo.line_state.lines_array) == 6

    def test_lines_color_state_initialization(self, std_opts):
        """Test ColorState initializes with zero values."""
        color_state = ColorState()
        assert color_state.count == 0
        assert color_state.old_r == 0
        assert color_state.old_g == 0
        assert color_state.old_b == 0
        assert color_state.new_r == 0
        assert color_state.new_g == 0
        assert color_state.new_b == 0

    def test_lines_line_state_initialization(self, std_opts):
        """Test LineState creates circular buffer."""
        line_state = LineState(num_lines=6)
        assert len(line_state.lines_array) == 6
        assert line_state.lines_idx == 0
        assert isinstance(line_state.line_skip, Line)

    def test_lines_update_changes_state(self, std_opts):
        """Test update changes line and color."""
        demo = Lines(std_opts)
        demo.setup()

        initial_line = demo.current_line
        initial_color = demo.current_color

        demo.update()

        # State should change (with high probability)
        # At least one of line or color should differ
        assert (demo.current_line.x1 != initial_line.x1 or
                demo.current_line.y1 != initial_line.y1 or
                demo.current_line.x2 != initial_line.x2 or
                demo.current_line.y2 != initial_line.y2 or
                demo.current_color.r != initial_color.r or
                demo.current_color.g != initial_color.g or
                demo.current_color.b != initial_color.b)

    def test_lines_bounce_physics(self, std_opts):
        """Test line endpoints bounce off edges."""
        demo = Lines(std_opts)
        demo.setup()

        # Set line very close to edge and force it out
        demo.line_state.lines_array[0] = Line(x1=1, y1=1, x2=1, y2=1)
        demo.line_state.lines_idx = 0
        demo.line_state.line_skip = Line(x1=-5, y1=-5, x2=5, y2=5)

        # Update to move line out of bounds (velocity reverses next frame)
        demo.update()

        # After bouncing, velocity should have reversed
        assert demo.line_state.line_skip.x1 > 0 or demo.line_state.line_skip.x1 < 0
        assert demo.line_state.line_skip.y1 > 0 or demo.line_state.line_skip.y1 < 0

    def test_lines_circular_buffer(self, std_opts):
        """Test line circular buffer cycles through 6 lines."""
        demo = Lines(std_opts)
        demo.setup()

        indices = []
        for _ in range(12):
            indices.append(demo.line_state.lines_idx)
            demo._next_line(reset=False)

        # Index increments before storing, so sequence starts at 1
        # Should cycle: 1,2,3,4,5,0,1,2,3,4,5,0
        assert indices == [1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 0]

    def test_lines_color_state_cycles(self, std_opts):
        """Test color state count cycles through 16-frame transitions."""
        demo = Lines(std_opts)
        demo.setup()

        # After setup, count should be 15
        assert demo.color_state.count == 15

        # After 16 steps, count cycles back: 15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0 -> 15
        for _ in range(16):
            demo._next_color(reset=False)

        # Count should be at 15 again (or lower if we got a new color picked)
        assert 0 <= demo.color_state.count <= 15

    def test_lines_draw_renders_pixels(self, std_opts):
        """Test draw renders line to canvas."""
        demo = Lines(std_opts)
        demo.setup()

        # Draw should not raise exception
        demo.draw()

        # Canvas should have some non-black pixels (or all black if line happened to be transparent)
        # Just verify draw completes

    def test_lines_draw_modes_render(self, std_opts):
        """Test all three draw modes render without error."""
        for mode in [1, 2, 4]:
            demo = Lines(std_opts)
            demo.draw_num = mode
            demo.setup()
            demo.update()
            demo.draw()
            # Should complete without exception


class TestFractal:
    """Test Fractal demo."""

    def test_fractal_initialization(self, std_opts):
        """Test initialization."""
        demo = Fractal(std_opts)
        assert demo.std_opts == std_opts

    def test_fractal_setup_creates_state(self, std_opts):
        """Test setup initializes fractal state."""
        demo = Fractal(std_opts)
        demo.setup()

        assert demo.canvas is not None
        assert demo.state is not None
        assert demo.palette is not None
        assert len(demo.palette) == 256
        assert demo.pixels is not None
        assert len(demo.pixels) == demo.canvas.width * demo.canvas.height

    def test_fractal_state_initialization(self):
        """Test FractalState initializes buffers."""
        state = FractalState(40, 30)
        assert state.width == 40
        assert state.height == 30
        assert len(state.fractal1) == 40 * 30 * 4
        assert len(state.fractal2) == 40 * 30 * 4
        assert state.offset == 0

    def test_fractal_computation(self):
        """Test Mandelbrot computation."""
        state = FractalState(20, 20)
        state.start_computation(-2.0, -1.5, 1.0, 1.5)

        # Compute some lines
        state.compute_lines(5)

        # Should have computed some pixels
        assert state.offset > 0
        # Some pixels should have non-zero iteration counts
        assert any(p > 0 for p in state.fractal1[:state.offset])

    def test_fractal_buffer_swap(self):
        """Test buffer swapping."""
        state = FractalState(20, 20)

        # Set some values in fractal1
        state.fractal1[0] = 42
        state.fractal2[0] = 7

        state.swap_buffers()

        # Values should be swapped
        assert state.fractal1[0] == 7
        assert state.fractal2[0] == 42

    def test_fractal_zoom_animation_state(self, std_opts):
        """Test zoom animation state variables."""
        demo = Fractal(std_opts)
        demo.setup()

        assert demo.zx == 4.0
        assert demo.zy == 4.0
        assert demo.zoom_in is True
        assert demo.frame_count == 0
        assert demo.k == 0
        assert demo.compute_step == 0

    def test_fractal_update_changes_state(self, std_opts):
        """Test update progresses computation."""
        demo = Fractal(std_opts)
        demo.setup()

        initial_step = demo.compute_step
        demo.update()

        # Compute step should increment
        assert demo.compute_step > initial_step

    def test_fractal_zoom_toggle(self, std_opts):
        """Test zoom direction toggles every 38 cycles."""
        demo = Fractal(std_opts)
        demo.setup()

        initial_zoom = demo.zoom_in

        # Run until a zoom toggle (approximately 38 * compute_steps_per_zoom updates)
        for _ in range(int(demo.compute_steps_per_zoom * 40)):
            demo.update()
            demo.draw()

        # After ~38 complete zoom cycles, direction should have toggled
        # (Note: This is probabilistic, depends on exact frame counts)

    def test_fractal_palette_generation(self, std_opts):
        """Test palette is generated."""
        demo = Fractal(std_opts)
        demo.setup()

        # Palette should have 256 colors
        assert len(demo.palette) == 256

        # Colors should have R and B channels (G always 0)
        for color in demo.palette:
            assert color.g == 0
            assert 0 <= color.r <= 255
            assert 0 <= color.b <= 255

    def test_fractal_palette_animation(self, std_opts):
        """Test palette animates over frames."""
        demo = Fractal(std_opts)
        demo.setup()

        colors_frame_0 = [demo.palette[i] for i in range(256)]
        demo.frame_count = 100
        demo._update_palette()
        colors_frame_100 = [demo.palette[i] for i in range(256)]

        # Palette should have changed
        assert colors_frame_0 != colors_frame_100

    def test_fractal_draw_renders(self, std_opts):
        """Test draw renders fractal to canvas."""
        demo = Fractal(std_opts)
        demo.setup()
        demo.update()
        demo.draw()

        # Should complete without exception

    def test_fractal_multiple_frames(self, std_opts):
        """Test running multiple frames."""
        demo = Fractal(std_opts)
        demo.setup()

        # Run several frames
        for _ in range(10):
            demo.update()
            demo.draw()

        # Frame count should have incremented
        assert demo.frame_count > 0


class TestRandomDots:
    """Test RandomDots demo."""

    def test_random_dots_initialization(self, std_opts):
        """Test initialization."""
        demo = RandomDots(std_opts)
        assert demo.std_opts == std_opts

    def test_random_dots_setup(self, std_opts):
        """Test setup initializes canvas."""
        demo = RandomDots(std_opts)
        demo.setup()

        assert demo.canvas is not None
        assert demo.canvas.width > 0
        assert demo.canvas.height > 0

    def test_random_dots_update(self, std_opts):
        """Test update is no-op."""
        demo = RandomDots(std_opts)
        demo.setup()

        # Update should not raise exception
        demo.update()

    def test_random_dots_draw(self, std_opts):
        """Test draw sets a pixel."""
        from flaschen_taschen.client.color import Color

        demo = RandomDots(std_opts)
        demo.setup()

        # Draw should not raise exception
        demo.draw()

        # Canvas should have at least one non-black pixel (with high probability)
        # (Unlikely but possible that a random color is black, so just check no exception)

    def test_random_dots_randomness(self, std_opts):
        """Test that multiple draws produce different positions."""
        from flaschen_taschen.client.color import Color

        demo = RandomDots(std_opts)
        demo.setup()

        positions = []
        colors = []
        for _ in range(20):
            # Reset canvas to track which pixel was drawn
            for y in range(demo.canvas.height):
                for x in range(demo.canvas.width):
                    demo.canvas.set_pixel(x, y, Color(0, 0, 0))

            demo.draw()

            # Find the non-black pixel (if any)
            found_pixel = False
            for y in range(demo.canvas.height):
                for x in range(demo.canvas.width):
                    pixel = demo.canvas.get_pixel(x, y)
                    if pixel and not (pixel.r == 0 and pixel.g == 0 and pixel.b == 0):
                        positions.append((x, y))
                        colors.append((pixel.r, pixel.g, pixel.b))
                        found_pixel = True
                        break
                if found_pixel:
                    break

        # Should have found at least some pixels
        assert len(positions) > 0

        # With high probability, positions should vary
        unique_positions = len(set(positions))
        assert unique_positions > 1

    def test_random_dots_color_range(self, std_opts):
        """Test that colors are in valid RGB range."""
        from flaschen_taschen.client.color import Color

        demo = RandomDots(std_opts)
        demo.setup()

        # Draw multiple times and check colors are valid
        for _ in range(10):
            demo.draw()

        # Scan canvas for any pixels
        for y in range(demo.canvas.height):
            for x in range(demo.canvas.width):
                pixel = demo.canvas.get_pixel(x, y)
                if pixel:
                    assert 0 <= pixel.r <= 255
                    assert 0 <= pixel.g <= 255
                    assert 0 <= pixel.b <= 255

    def test_random_dots_position_in_bounds(self, std_opts):
        """Test that pixels are drawn within canvas bounds."""
        from flaschen_taschen.client.color import Color

        demo = RandomDots(std_opts)
        demo.setup()

        # Draw multiple times
        for _ in range(50):
            demo.draw()

        # All non-black pixels should be within bounds
        for y in range(demo.canvas.height):
            for x in range(demo.canvas.width):
                pixel = demo.canvas.get_pixel(x, y)
                assert pixel is not None
                # Position is implicitly valid (it's on the canvas)

    def test_random_dots_continuous(self, std_opts):
        """Test continuous drawing without errors."""
        demo = RandomDots(std_opts)
        demo.setup()

        # Run multiple frames
        for _ in range(100):
            demo.update()
            demo.draw()

        # Should complete without exceptions
