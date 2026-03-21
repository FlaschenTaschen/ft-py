"""Tests for bitmap font module."""

import pytest
from flaschen_taschen.utils.bitmap_font import BitmapFont


class TestBitmapFont:
    """Test BitmapFont class."""

    def test_render_char_space(self):
        """Test rendering space character."""
        bitmap = BitmapFont.render_char(' ')
        assert len(bitmap) == 5
        assert all(len(row) == 5 for row in bitmap)
        assert all(pixel == 0 for row in bitmap for pixel in row)

    def test_render_char_A(self):
        """Test rendering 'A' character."""
        bitmap = BitmapFont.render_char('A')
        assert len(bitmap) == 5
        assert all(len(row) == 5 for row in bitmap)
        # Should have some pixels set
        assert any(pixel == 1 for row in bitmap for pixel in row)

    def test_render_char_scale_2(self):
        """Test rendering character with scale=2."""
        bitmap = BitmapFont.render_char('A', scale=2)
        assert len(bitmap) == 10
        assert all(len(row) == 10 for row in bitmap)

    def test_render_char_unknown(self):
        """Test rendering unknown character (should use space)."""
        bitmap = BitmapFont.render_char('\x00')
        # Unknown char should render as space
        assert all(pixel == 0 for row in bitmap for pixel in row)

    def test_get_text_width(self):
        """Test text width calculation."""
        width = BitmapFont.get_text_width('Hello', scale=1)
        assert width == 5 * 5  # 5 chars * 5 width

        width = BitmapFont.get_text_width('Hello', scale=2)
        assert width == 5 * 10  # 5 chars * 10 width

    def test_get_text_height(self):
        """Test text height calculation."""
        height = BitmapFont.get_text_height(scale=1)
        assert height == 5

        height = BitmapFont.get_text_height(scale=2)
        assert height == 10

    def test_all_printable_chars_available(self):
        """Test that all common ASCII characters are available."""
        test_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()'
        for char in test_chars:
            bitmap = BitmapFont.render_char(char)
            assert len(bitmap) == 5
            assert all(len(row) == 5 for row in bitmap)
