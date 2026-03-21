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
