"""Tests for the debugger module."""

import pytest

from flaschen_taschen.client.color import Color, create_hsv_palette
from flaschen_taschen.debugger import DisplayDebugger, Mode


@pytest.fixture
def debugger():
    """Create a test debugger instance."""
    palette = create_hsv_palette(256).colors
    return DisplayDebugger(mode=Mode.EDGES, palette=palette)


class TestDisplayDebugger:
    """Test DisplayDebugger class."""

    def test_init_edges_mode(self):
        """Test initialization with edges mode."""
        palette = create_hsv_palette(256).colors
        debugger = DisplayDebugger(mode=Mode.EDGES, palette=palette)
        assert debugger.mode == Mode.EDGES
        assert len(debugger.palette) == 256

    def test_init_fill_mode(self):
        """Test initialization with fill mode."""
        palette = create_hsv_palette(256).colors
        debugger = DisplayDebugger(mode=Mode.FILL, palette=palette)
        assert debugger.mode == Mode.FILL

    def test_draw_edges(self, debugger):
        """Test drawing edges."""
        color = Color(255, 0, 0)
        debugger.draw_edges(color)
        # Check that edge pixels are set
        assert debugger.canvas.get_pixel(0, 0) == color
        assert debugger.canvas.get_pixel(debugger.config.width - 1, 0) == color

    def test_draw_fill(self, debugger):
        """Test drawing fill."""
        color = Color(0, 255, 0)
        debugger.draw_fill(color)
        # Check that all pixels are set to the color
        assert debugger.canvas.get_pixel(10, 10) == color
        assert debugger.canvas.get_pixel(20, 20) == color

    def test_default_palette(self):
        """Test that default palette is created."""
        debugger = DisplayDebugger(mode=Mode.EDGES)
        assert len(debugger.palette) == 256
        # Check that colors vary
        assert debugger.palette[0] != debugger.palette[128]

    def test_custom_palette(self):
        """Test initialization with custom palette."""
        custom_palette = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]
        debugger = DisplayDebugger(mode=Mode.EDGES, palette=custom_palette)
        assert len(debugger.palette) == 3
        assert debugger.palette[0].r == 255
