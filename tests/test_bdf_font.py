"""Tests for BDF font parser."""

import pytest
import os
import tempfile
from flaschen_taschen.utils.bdf_font import BDFFont


class TestBDFFont:
    """Test BDFFont class."""

    def test_load_real_font(self):
        """Test loading a real 5x5.bdf font file."""
        # Try to load the actual 5x5 font
        font_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'flaschen-taschen',
            'client',
            'fonts',
            '5x5.bdf'
        )

        if os.path.exists(font_path):
            font = BDFFont(font_path)
            assert font.char_width > 0
            assert font.char_height > 0
            assert len(font.characters) > 0

            # Test rendering a character
            bitmap = font.render_char('A')
            assert bitmap is not None
            assert len(bitmap) == font.char_height
            assert all(len(row) == font.char_width for row in bitmap)

    def test_font_not_found(self):
        """Test that FileNotFoundError is raised for missing fonts."""
        with pytest.raises(FileNotFoundError):
            BDFFont('/nonexistent/path/font.bdf')

    def test_get_text_width(self):
        """Test text width calculation."""
        font_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'flaschen-taschen',
            'client',
            'fonts',
            '5x5.bdf'
        )

        if os.path.exists(font_path):
            font = BDFFont(font_path)
            width = font.get_text_width('Hi')
            assert width > 0

    def test_get_text_height(self):
        """Test text height."""
        font_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'flaschen-taschen',
            'client',
            'fonts',
            '5x5.bdf'
        )

        if os.path.exists(font_path):
            font = BDFFont(font_path)
            height = font.get_text_height()
            assert height > 0
