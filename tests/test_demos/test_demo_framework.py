"""Tests for the Demo framework base class."""

import pytest
from flaschen_taschen.demos import Demo
from flaschen_taschen.standard_options import StandardOptions


class SimpleTestDemo(Demo):
    """Simple test demo for testing framework."""

    def setup(self) -> None:
        """Set up test demo."""
        super().setup()
        self.update_count = 0
        self.draw_count = 0

    def update(self) -> None:
        """Count updates."""
        self.update_count += 1

    def draw(self) -> None:
        """Count draws."""
        self.draw_count += 1


class TestDemoFramework:
    """Test the base Demo class functionality."""

    def test_demo_initialization(self):
        """Test demo initialization with standard options."""
        opts = StandardOptions(["-g", "40x30", "-h", "test.local", "-t", "1"])
        demo = SimpleTestDemo(opts)

        assert demo.std_opts == opts
        assert demo.canvas is None
        assert demo._frame_count == 0

    def test_demo_setup(self):
        """Test demo setup creates canvas."""
        opts = StandardOptions(["-g", "40x30"])
        demo = SimpleTestDemo(opts)

        demo.setup()

        assert demo.canvas is not None
        assert demo.canvas.width == 40
        assert demo.canvas.height == 30

    def test_demo_geometry_parsing(self):
        """Test demo geometry parsing from standard options."""
        opts = StandardOptions(["-g", "50x40+10+5"])
        demo = SimpleTestDemo(opts)

        demo.setup()

        assert demo.canvas is not None
        assert demo.std_opts.width == 50
        assert demo.std_opts.height == 40
        assert demo.std_opts.xoff == 10
        assert demo.std_opts.yoff == 5

    def test_demo_update_and_draw(self):
        """Test update and draw lifecycle."""
        opts = StandardOptions(["-t", "1"])
        demo = SimpleTestDemo(opts)

        demo.setup()
        demo.update()
        demo.draw()

        assert demo.update_count == 1
        assert demo.draw_count == 1

    def test_demo_send_increments_frame(self):
        """Test that send increments frame count."""
        opts = StandardOptions(["-t", "1"])
        demo = SimpleTestDemo(opts)

        demo.setup()

        assert demo._frame_count == 0
        demo.send()
        assert demo._frame_count == 1
        demo.send()
        assert demo._frame_count == 2

    def test_demo_fps_calculation(self):
        """Test FPS calculation."""
        import time

        opts = StandardOptions(["-t", "1"])
        demo = SimpleTestDemo(opts)

        demo.setup()

        # Send a few frames with small delay
        for _ in range(5):
            demo.send()
            time.sleep(0.001)

        fps = demo.fps
        assert fps > 0  # Should have non-zero FPS

    def test_demo_cleanup(self):
        """Test demo cleanup."""
        opts = StandardOptions(["-t", "1"])
        demo = SimpleTestDemo(opts)

        demo.setup()
        assert demo.canvas is not None
        assert demo.canvas.connection is not None

        # Cleanup should close connection
        demo.cleanup()
        # Connection should be closed (no exception on cleanup)

    def test_demo_delay_option(self):
        """Test frame delay option."""
        opts = StandardOptions(["-d", "10", "-t", "1"])
        demo = SimpleTestDemo(opts)

        assert demo.std_opts.delay == 10

    def test_demo_timeout_option(self):
        """Test timeout option."""
        opts = StandardOptions(["-t", "5"])
        demo = SimpleTestDemo(opts)

        assert demo.std_opts.timeout == 5

    def test_demo_host_option(self):
        """Test host option."""
        opts = StandardOptions(["-h", "display.local"])
        demo = SimpleTestDemo(opts)

        assert demo.std_opts.hostname == "display.local"

    def test_demo_layer_option(self):
        """Test layer option."""
        opts = StandardOptions(["-l", "5"])
        demo = SimpleTestDemo(opts)

        assert demo.std_opts.layer == 5

    def test_demo_invalid_geometry(self):
        """Test error handling for invalid geometry."""
        with pytest.raises(ValueError):
            StandardOptions(["-g", "invalidxgeometry"])

    def test_demo_negative_geometry(self):
        """Test error handling for negative dimensions."""
        with pytest.raises(ValueError):
            StandardOptions(["-g", "0x20"])  # Width of 0 is invalid
