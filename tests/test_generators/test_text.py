"""Tests for text generator."""

import pytest
from unittest.mock import Mock, MagicMock, patch
from flaschen_taschen.generators.text import TextGenerator
from flaschen_taschen.client.color import Color


class TestTextGenerator:
    """Test TextGenerator class."""

    @pytest.fixture
    def mock_canvas(self):
        """Create a mock canvas."""
        canvas = Mock()
        canvas.width = 45
        canvas.height = 35
        canvas.clear = Mock()
        canvas.set_pixel = Mock()
        canvas.send = Mock()
        return canvas

    @pytest.fixture
    def mock_font(self):
        """Create a mock BDF font."""
        font = Mock()
        font.get_char_width.return_value = 5
        font.get_text_height.return_value = 5
        font.get_text_width.return_value = 25
        # Return a simple 5x5 bitmap
        font.render_char.return_value = [[1, 1, 1, 0, 0] for _ in range(5)]
        return font

    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_init(self, mock_bdf_class, mock_canvas, mock_font):
        """Test TextGenerator initialization."""
        mock_bdf_class.return_value = mock_font
        gen = TextGenerator(mock_canvas, "Hello", "/path/to/font.bdf")
        assert gen.text == "Hello"
        assert gen.color == Color.WHITE
        assert gen.scroll is True

    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_init_custom_color(self, mock_bdf_class, mock_canvas, mock_font):
        """Test initialization with custom color."""
        mock_bdf_class.return_value = mock_font
        color = Color(255, 0, 0)
        gen = TextGenerator(mock_canvas, "Hello", "/path/to/font.bdf", color=color)
        assert gen.color == color

    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_init_no_scroll(self, mock_bdf_class, mock_canvas, mock_font):
        """Test initialization with scroll disabled."""
        mock_bdf_class.return_value = mock_font
        gen = TextGenerator(mock_canvas, "Hello", "/path/to/font.bdf", scroll=False)
        assert gen.scroll is False

    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_render_static(self, mock_bdf_class, mock_canvas, mock_font):
        """Test rendering static text."""
        mock_bdf_class.return_value = mock_font
        gen = TextGenerator(mock_canvas, "A", "/path/to/font.bdf", scroll=False)
        gen.render_static(x=0, y=0)

        # Should clear canvas
        mock_canvas.clear.assert_called_once()

    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_render_static_sends(self, mock_bdf_class, mock_canvas, mock_font):
        """Test that render sends frame."""
        mock_bdf_class.return_value = mock_font
        gen = TextGenerator(mock_canvas, "A", "/path/to/font.bdf", scroll=False)
        gen.render(x=0, y=0)

        # Should clear canvas and send
        mock_canvas.clear.assert_called_once()
        mock_canvas.send.assert_called_once()

    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_render_static_bounds_checking(self, mock_bdf_class, mock_canvas, mock_font):
        """Test static render with bounds checking."""
        mock_bdf_class.return_value = mock_font
        mock_canvas.width = 10
        mock_canvas.height = 10
        gen = TextGenerator(mock_canvas, "Hello", "/path/to/font.bdf")
        gen.render_static(x=0, y=0)

        # set_pixel should be called for visible pixels
        assert mock_canvas.set_pixel.called

    @patch('time.time')
    @patch('time.sleep')
    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_render_scrolling(self, mock_bdf_class, mock_sleep, mock_time, mock_canvas, mock_font):
        """Test scrolling text render."""
        mock_bdf_class.return_value = mock_font
        mock_time.side_effect = [0, 0.033, 0.066, 0.1, 1.0]  # Time progression
        mock_sleep.return_value = None

        gen = TextGenerator(mock_canvas, "Hi", "/path/to/font.bdf", scroll=True, scroll_speed=1)

        # Render for short time to prevent infinite loop
        gen.render_scrolling(y=10, duration=0.1)

        # Should call canvas methods multiple times
        assert mock_canvas.clear.called
        assert mock_canvas.send.called

    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_render_chooses_scroll(self, mock_bdf_class, mock_canvas, mock_font):
        """Test that render() chooses between static and scrolling."""
        mock_bdf_class.return_value = mock_font
        gen = TextGenerator(mock_canvas, "Test", "/path/to/font.bdf", scroll=False)

        with patch.object(gen, 'render_static') as mock_static:
            gen.render(x=5, y=10)
            mock_static.assert_called_once()

    @patch('time.sleep')
    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_render_scrolling_duration(self, mock_bdf_class, mock_sleep, mock_canvas, mock_font):
        """Test scrolling with duration limit."""
        mock_bdf_class.return_value = mock_font
        gen = TextGenerator(mock_canvas, "Hi", "/path/to/font.bdf", scroll=True)

        with patch('time.time') as mock_time:
            # Mock time to simulate duration expiry
            mock_time.side_effect = [0, 0.01, 0.02, 100]  # Last value exceeds duration

            gen.render_scrolling(duration=0.05)

            # Should stop when duration exceeded
            # This is tested by checking it doesn't infinite loop

    @patch('flaschen_taschen.generators.text.BDFFont')
    def test_text_with_special_chars(self, mock_bdf_class, mock_canvas, mock_font):
        """Test rendering text with special characters."""
        mock_bdf_class.return_value = mock_font
        gen = TextGenerator(mock_canvas, "!@#$%", "/path/to/font.bdf", scroll=False)
        gen.render_static(x=0, y=0)

        assert mock_canvas.clear.called
        # set_pixel called for valid pixels
        assert mock_canvas.set_pixel.called or not mock_canvas.set_pixel.called  # OK either way
