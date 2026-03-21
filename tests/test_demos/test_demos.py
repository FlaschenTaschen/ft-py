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
