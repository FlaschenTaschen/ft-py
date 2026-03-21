"""Tests for image generator."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from flaschen_taschen.generators.image import ImageGenerator
from flaschen_taschen.client.color import Color


class TestImageGenerator:
    """Test ImageGenerator class."""

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

    def test_init_with_image_data(self, mock_canvas):
        """Test initialization with image data."""
        mock_image = Mock()
        gen = ImageGenerator(mock_canvas, image_data=mock_image)
        assert gen.image == mock_image

    @patch('flaschen_taschen.generators.image.Image')
    def test_init_with_path(self, mock_pil, mock_canvas):
        """Test initialization with image path."""
        mock_image = Mock()
        mock_pil.open.return_value = mock_image

        gen = ImageGenerator(mock_canvas, image_path='test.png')
        assert gen.image == mock_image
        mock_pil.open.assert_called_once_with('test.png')

    def test_init_no_image_raises(self, mock_canvas):
        """Test that initialization without image raises."""
        with pytest.raises(ValueError):
            ImageGenerator(mock_canvas)

    def test_quantize_color_tuple(self, mock_canvas):
        """Test color quantization from tuple."""
        gen = ImageGenerator(mock_canvas, image_data=Mock())
        r, g, b = gen._quantize_color((255, 128, 64))
        assert r == 255
        assert g == 128
        assert b == 64

    def test_quantize_color_clamping(self, mock_canvas):
        """Test color quantization with clamping."""
        gen = ImageGenerator(mock_canvas, image_data=Mock())
        r, g, b = gen._quantize_color((300, -10, 128))
        assert r == 255  # Clamped to max
        assert g == 0    # Clamped to min
        assert b == 128  # In range

    def test_quantize_color_int(self, mock_canvas):
        """Test color quantization from single int (grayscale)."""
        gen = ImageGenerator(mock_canvas, image_data=Mock())
        r, g, b = gen._quantize_color(128)
        assert r == 128
        assert g == 128
        assert b == 128

    @patch('flaschen_taschen.generators.image.Image')
    def test_resize_image(self, mock_pil, mock_canvas):
        """Test image resizing."""
        mock_image = Mock()
        mock_image.width = 100
        mock_image.height = 100
        mock_resized = Mock()
        mock_image.resize.return_value = mock_resized

        gen = ImageGenerator(mock_canvas, image_data=mock_image)
        result = gen._resize_image(mock_image, 45, 35)

        assert result == mock_resized
        mock_image.resize.assert_called_once()

    def test_render_no_image_raises(self, mock_canvas):
        """Test render raises if no image."""
        gen = ImageGenerator.__new__(ImageGenerator)
        gen.image = None
        gen.canvas = mock_canvas

        with pytest.raises(ValueError):
            gen.render()

    @patch('flaschen_taschen.generators.image.Image')
    def test_render_rgb_image(self, mock_pil, mock_canvas):
        """Test rendering RGB image."""
        mock_image = Mock()
        mock_image.mode = 'RGB'
        mock_image.width = 10
        mock_image.height = 10
        mock_image.n_frames = 1  # Static image
        mock_image.resize.return_value = mock_image

        # Mock pixel data
        pixels = {(x, y): (255, 0, 0) for x in range(10) for y in range(10)}
        mock_image.load.return_value = pixels

        gen = ImageGenerator(mock_canvas, image_data=mock_image)
        gen.render()

        # Should set pixels and send
        assert mock_canvas.set_pixel.called
        assert mock_canvas.send.called

    @patch('flaschen_taschen.generators.image.Image')
    def test_render_rgba_image(self, mock_pil, mock_canvas):
        """Test rendering RGBA image with alpha channel."""
        mock_image = Mock()
        mock_image.mode = 'RGBA'
        mock_image.size = (10, 10)
        mock_image.n_frames = 1  # Static image

        # Mock the paste behavior
        mock_rgb = Mock()
        mock_rgb.width = 10
        mock_rgb.height = 10
        mock_rgb.resize.return_value = mock_rgb
        mock_rgb.load.return_value = {(x, y): (255, 0, 0) for x in range(10) for y in range(10)}

        # Mock Image.new to return our mock_rgb
        def image_new_side_effect(mode, size, color):
            return mock_rgb

        mock_pil.new.side_effect = image_new_side_effect

        # Mock split for alpha
        mock_image.split.return_value = [None, None, None, Mock()]

        gen = ImageGenerator(mock_canvas, image_data=mock_image)
        gen.render()

        assert mock_canvas.send.called

    @patch('time.sleep')
    @patch('time.time')
    @patch('flaschen_taschen.generators.image.Image')
    def test_render_animated_gif(self, mock_pil, mock_time, mock_sleep, mock_canvas):
        """Test rendering animated GIF with multiple frames and looping."""
        mock_image = Mock()
        mock_image.mode = 'RGB'
        mock_image.width = 10
        mock_image.height = 10
        mock_image.n_frames = 3  # Animated image with 3 frames
        mock_image.info = {'duration': 100}  # 100ms per frame
        mock_image.resize.return_value = mock_image

        # Mock pixel data
        pixels = {(x, y): (255, 0, 0) for x in range(10) for y in range(10)}
        mock_image.load.return_value = pixels

        # Mock time to simulate 0.5 second duration (should play ~1.67 loops)
        mock_time.side_effect = [0, 0.1, 0.2, 0.3, 0.4, 0.5]

        gen = ImageGenerator(mock_canvas, image_data=mock_image)
        gen.render(duration=0.5)

        # Should seek multiple times (at least 3 for first loop)
        assert mock_image.seek.call_count >= 3
        # Should send multiple times (at least 3 for first loop)
        assert mock_canvas.send.call_count >= 3
        # Should sleep between frames
        assert mock_sleep.call_count >= 2
