"""Tests for Color module."""

import pytest

from flaschen_taschen.client.color import Color, ColorPalette, create_hsv_palette, hsv_to_rgb


class TestColor:
    """Test Color class functionality."""

    def test_color_creation_rgb(self):
        """Test creating color with RGB values."""
        color = Color(255, 128, 64)
        assert color.r == 255
        assert color.g == 128
        assert color.b == 64

    def test_color_creation_from_tuple(self):
        """Test creating color from tuple."""
        color = Color((100, 150, 200))
        assert color.r == 100
        assert color.g == 150
        assert color.b == 200

    def test_color_creation_from_color(self):
        """Test creating color from another color."""
        original = Color(50, 100, 150)
        copy = Color(original)
        assert copy.r == 50
        assert copy.g == 100
        assert copy.b == 150

    def test_color_creation_hex(self):
        """Test creating color from hex string."""
        color = Color("#FF8040")
        assert color.r == 255
        assert color.g == 128
        assert color.b == 64

    def test_color_clamping(self):
        """Test that values are clamped to 0-255."""
        color = Color(300, -10, 128)
        assert color.r == 255
        assert color.g == 0
        assert color.b == 128

    def test_color_to_hex(self):
        """Test converting color to hex string."""
        color = Color(255, 128, 64)
        assert color.to_hex() == "#ff8040"

    def test_color_to_tuple(self):
        """Test converting color to tuple."""
        color = Color(100, 150, 200)
        assert color.to_tuple() == (100, 150, 200)

    def test_color_equality(self):
        """Test color equality comparison."""
        color1 = Color(100, 150, 200)
        color2 = Color(100, 150, 200)
        color3 = Color(50, 75, 100)

        assert color1 == color2
        assert color1 != color3

    def test_named_colors(self):
        """Test predefined named colors."""
        assert Color.BLACK == Color(0, 0, 0)
        assert Color.WHITE == Color(255, 255, 255)
        assert Color.RED == Color(255, 0, 0)
        assert Color.GREEN == Color(0, 255, 0)
        assert Color.BLUE == Color(0, 0, 255)


class TestColorPalette:
    """Test ColorPalette class."""

    def test_palette_creation(self):
        """Test creating a palette."""
        colors = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]
        palette = ColorPalette(colors)
        assert len(palette) == 3

    def test_palette_get_color(self):
        """Test getting color from palette."""
        colors = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]
        palette = ColorPalette(colors)

        assert palette.get_color(0) == colors[0]
        assert palette.get_color(1) == colors[1]
        assert palette.get_color(2) == colors[2]

    def test_palette_wrapping(self):
        """Test palette color index wrapping."""
        colors = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]
        palette = ColorPalette(colors)

        # Index wrapping
        assert palette.get_color(3) == colors[0]
        assert palette.get_color(4) == colors[1]
        assert palette.get_color(6) == colors[0]

    def test_palette_indexing(self):
        """Test palette indexing with [] operator."""
        colors = [Color(255, 0, 0), Color(0, 255, 0)]
        palette = ColorPalette(colors)

        assert palette[0] == colors[0]
        assert palette[1] == colors[1]
        assert palette[2] == colors[0]  # Wrapping


class TestHSVConversion:
    """Test HSV to RGB conversion."""

    def test_hsv_pure_red(self):
        """Test HSV red conversion."""
        r, g, b = hsv_to_rgb(0, 1, 1)
        assert r > 200  # Should be close to 255
        assert g < 55  # Should be close to 0
        assert b < 55  # Should be close to 0

    def test_hsv_pure_green(self):
        """Test HSV green conversion."""
        r, g, b = hsv_to_rgb(1 / 3, 1, 1)
        assert r < 55
        assert g > 200
        assert b < 55

    def test_hsv_grayscale(self):
        """Test HSV grayscale (s=0)."""
        r, g, b = hsv_to_rgb(0, 0, 0.5)
        # All channels should be equal for grayscale
        assert abs(r - g) < 10
        assert abs(g - b) < 10

    def test_hsv_palette_creation(self):
        """Test creating HSV palette."""
        palette = create_hsv_palette(8)
        assert len(palette) == 8

        # Each color should be different
        colors = [palette.get_color(i) for i in range(8)]
        unique_colors = set(c.to_hex() for c in colors)
        assert len(unique_colors) > 1  # At least more than one unique color


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
