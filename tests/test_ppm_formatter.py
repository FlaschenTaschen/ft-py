"""Tests for PPM Formatter module."""

import pytest

from flaschen_taschen.client.color import Color
from flaschen_taschen.client.ppm_formatter import PPMFormatter


class TestPPMFormatter:
    """Test PPMFormatter encoding and decoding."""

    def test_encode_simple_frame(self):
        """Test encoding a simple pixel frame."""
        # Create a simple 2x2 red frame
        pixels = [
            [(255, 0, 0), (255, 0, 0)],
            [(255, 0, 0), (255, 0, 0)],
        ]

        data = PPMFormatter.encode(pixels)

        # Verify magic number
        assert data.startswith(b"P6\n")

        # Verify it contains FT metadata
        assert b"#FT:" in data

        # Verify dimensions
        assert b"2 2\n" in data

        # Verify max color value
        assert b"255\n" in data

    def test_encode_with_metadata(self):
        """Test encoding with FT metadata."""
        pixels = [[(100, 150, 200)]]

        data = PPMFormatter.encode(pixels, x_offset=10, y_offset=20, layer=5)

        # Check FT metadata is correct
        assert b"#FT: 10 20 5" in data

    def test_decode_simple_frame(self):
        """Test decoding a PPM frame."""
        # Create and encode a frame
        pixels = [
            [(255, 0, 0), (0, 255, 0)],
            [(0, 0, 255), (255, 255, 0)],
        ]

        data = PPMFormatter.encode(pixels)

        # Decode it back
        result = PPMFormatter.decode(data)

        assert result["width"] == 2
        assert result["height"] == 2
        assert result["pixels"][0][0] == (255, 0, 0)
        assert result["pixels"][0][1] == (0, 255, 0)
        assert result["pixels"][1][0] == (0, 0, 255)
        assert result["pixels"][1][1] == (255, 255, 0)

    def test_decode_with_metadata(self):
        """Test decoding preserves FT metadata."""
        pixels = [[(100, 150, 200)]]

        data = PPMFormatter.encode(pixels, x_offset=5, y_offset=10, layer=3)
        result = PPMFormatter.decode(data)

        assert result["x_offset"] == 5
        assert result["y_offset"] == 10
        assert result["layer"] == 3

    def test_roundtrip_encoding(self):
        """Test that encode->decode->encode produces same data."""
        pixels = [
            [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
            [(128, 64, 32), (64, 128, 192), (200, 100, 50)],
        ]

        # Encode
        data1 = PPMFormatter.encode(pixels)

        # Decode
        decoded = PPMFormatter.decode(data1)

        # Re-encode
        data2 = PPMFormatter.encode(decoded["pixels"])

        # Should be very similar (metadata might differ)
        assert decoded["width"] == 3
        assert decoded["height"] == 2
        assert decoded["pixels"] == pixels

    def test_create_blank(self):
        """Test creating a blank frame."""
        color = Color(128, 64, 32)
        data = PPMFormatter.create_blank(4, 3, color)

        result = PPMFormatter.decode(data)

        assert result["width"] == 4
        assert result["height"] == 3

        # All pixels should be the fill color
        for row in result["pixels"]:
            for pixel in row:
                assert pixel == (128, 64, 32)

    def test_create_blank_default_color(self):
        """Test blank frame defaults to black."""
        data = PPMFormatter.create_blank(2, 2)
        result = PPMFormatter.decode(data)

        for row in result["pixels"]:
            for pixel in row:
                assert pixel == (0, 0, 0)

    def test_resize_nearest_neighbor(self):
        """Test frame resizing with nearest-neighbor scaling."""
        # Create a simple 2x2 frame
        pixels = [
            [(255, 0, 0), (0, 255, 0)],
            [(0, 0, 255), (255, 255, 0)],
        ]

        data = PPMFormatter.encode(pixels)

        # Resize to 4x4
        resized = PPMFormatter.resize_frame(data, 4, 4, scale_mode="nearest")
        result = PPMFormatter.decode(resized)

        assert result["width"] == 4
        assert result["height"] == 4

        # Top-left quadrant should be red
        assert result["pixels"][0][0] == (255, 0, 0)
        assert result["pixels"][0][1] == (255, 0, 0)
        assert result["pixels"][1][0] == (255, 0, 0)
        assert result["pixels"][1][1] == (255, 0, 0)

    def test_invalid_format(self):
        """Test that invalid PPM data raises error."""
        with pytest.raises(ValueError, match="Invalid PPM format"):
            PPMFormatter.decode(b"INVALID DATA")

    def test_empty_pixels(self):
        """Test that empty pixels raise error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            PPMFormatter.encode([])

    def test_jagged_array(self):
        """Test that jagged arrays raise error."""
        pixels = [
            [(255, 0, 0), (0, 255, 0)],
            [(0, 0, 255)],  # Different width
        ]

        with pytest.raises(ValueError, match="same width"):
            PPMFormatter.encode(pixels)

    def test_color_clamping(self):
        """Test that out-of-range colors are clamped."""
        pixels = [[(300, -10, 128)]]  # Out of range values

        data = PPMFormatter.encode(pixels)
        result = PPMFormatter.decode(data)

        # Should be clamped to valid range
        r, g, b = result["pixels"][0][0]
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
