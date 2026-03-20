"""Tests for Canvas module."""

import pytest

from flaschen_taschen.client.canvas import Canvas
from flaschen_taschen.client.color import Color
from flaschen_taschen.client.config import Config


class TestCanvas:
    """Test Canvas class functionality."""

    def test_canvas_creation(self):
        """Test creating a canvas with default config."""
        canvas = Canvas()
        assert canvas.width == 45
        assert canvas.height == 35
        assert canvas.auto_send is True

    def test_canvas_with_custom_config(self):
        """Test canvas with custom configuration."""
        config = Config(width=32, height=24, host="localhost")
        canvas = Canvas(config)
        assert canvas.width == 32
        assert canvas.height == 24

    def test_canvas_auto_send_disabled(self):
        """Test canvas with auto_send disabled."""
        canvas = Canvas(auto_send=False)
        assert canvas.auto_send is False

    def test_set_pixel(self):
        """Test setting individual pixels."""
        canvas = Canvas()
        color = Color(255, 0, 0)

        canvas.set_pixel(10, 10, color)

        # Verify pixel was set
        retrieved = canvas.get_pixel(10, 10)
        assert retrieved == color

    def test_get_pixel_out_of_bounds(self):
        """Test getting pixel outside canvas."""
        canvas = Canvas()

        result = canvas.get_pixel(100, 100)
        assert result is None

        result = canvas.get_pixel(-1, -1)
        assert result is None

    def test_set_pixel_out_of_bounds(self):
        """Test setting pixel outside canvas (should be ignored)."""
        canvas = Canvas()
        color = Color(255, 0, 0)

        # Should not raise, just ignore
        canvas.set_pixel(1000, 1000, color)

    def test_clear_canvas(self):
        """Test clearing the canvas."""
        canvas = Canvas()

        # Set some pixels
        canvas.set_pixel(0, 0, Color.RED)
        canvas.set_pixel(5, 5, Color.GREEN)

        # Clear with black
        canvas.clear(Color.BLACK)

        # All pixels should be black
        assert canvas.get_pixel(0, 0) == Color.BLACK
        assert canvas.get_pixel(5, 5) == Color.BLACK

    def test_clear_default_color(self):
        """Test clear defaults to black."""
        canvas = Canvas()
        canvas.set_pixel(0, 0, Color.RED)

        canvas.clear()

        assert canvas.get_pixel(0, 0) == Color.BLACK

    def test_fill_rect(self):
        """Test filling a rectangle."""
        canvas = Canvas()
        color = Color(100, 150, 200)

        canvas.fill_rect(5, 5, 3, 3, color)

        # Check corners and center
        assert canvas.get_pixel(5, 5) == color
        assert canvas.get_pixel(7, 7) == color
        assert canvas.get_pixel(5, 7) == color
        assert canvas.get_pixel(7, 5) == color

        # Check outside area is still black
        assert canvas.get_pixel(4, 4) == Color.BLACK
        assert canvas.get_pixel(8, 8) == Color.BLACK

    def test_draw_line(self):
        """Test drawing a line."""
        canvas = Canvas()
        color = Color(255, 255, 255)

        # Draw horizontal line
        canvas.draw_line(5, 5, 10, 5, color)

        # Check line pixels
        for x in range(5, 11):
            assert canvas.get_pixel(x, 5) == color

    def test_draw_line_vertical(self):
        """Test drawing a vertical line."""
        canvas = Canvas()
        color = Color(255, 255, 255)

        canvas.draw_line(5, 5, 5, 10, color)

        # Check line pixels
        for y in range(5, 11):
            assert canvas.get_pixel(5, y) == color

    def test_draw_line_diagonal(self):
        """Test drawing a diagonal line."""
        canvas = Canvas()
        color = Color(128, 128, 128)

        canvas.draw_line(0, 0, 5, 5, color)

        # Start and end should be colored
        assert canvas.get_pixel(0, 0) == color
        assert canvas.get_pixel(5, 5) == color

    def test_draw_circle(self):
        """Test drawing a circle outline."""
        canvas = Canvas()
        color = Color(200, 100, 50)

        canvas.draw_circle(22, 17, 5, color, filled=False)

        # Center should be black (not filled)
        assert canvas.get_pixel(22, 17) == Color.BLACK

        # Edge should have some colored pixels
        edge_pixels = [
            canvas.get_pixel(27, 17),
            canvas.get_pixel(17, 17),
            canvas.get_pixel(22, 22),
        ]
        assert any(p == color for p in edge_pixels)

    def test_draw_circle_filled(self):
        """Test drawing a filled circle."""
        canvas = Canvas()
        color = Color(200, 100, 50)

        canvas.draw_circle(22, 17, 5, color, filled=True)

        # Center should be colored
        assert canvas.get_pixel(22, 17) == color

    def test_frame_info(self):
        """Test getting frame statistics."""
        canvas = Canvas()

        info = canvas.get_frame_info()

        assert "frame_count" in info
        assert "elapsed_time" in info
        assert "fps" in info
        assert info["frame_count"] == 0

    def test_dirty_flag(self):
        """Test dirty flag tracking."""
        canvas = Canvas(auto_send=False)

        assert canvas.dirty is True

        canvas.set_pixel(0, 0, Color.RED)
        assert canvas.dirty is True

    def test_context_manager(self):
        """Test using canvas as context manager."""
        with Canvas() as canvas:
            canvas.set_pixel(0, 0, Color.RED)
            assert canvas.get_pixel(0, 0) == Color.RED

        # After exit, connection should be closed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
