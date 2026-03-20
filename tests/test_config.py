"""Tests for Config module."""

import pytest

from flaschen_taschen.client.config import Config


class TestConfig:
    """Test Config class functionality."""

    def test_default_config(self):
        """Test creating config with all defaults."""
        config = Config()

        assert config.width == Config.DEFAULT_WIDTH
        assert config.height == Config.DEFAULT_HEIGHT
        assert config.x_offset == Config.DEFAULT_X_OFFSET
        assert config.y_offset == Config.DEFAULT_Y_OFFSET
        assert config.host == Config.DEFAULT_HOST
        assert config.port == Config.DEFAULT_PORT
        assert config.frame_delay_ms == Config.DEFAULT_FRAME_DELAY_MS
        assert config.timeout_seconds == Config.DEFAULT_TIMEOUT_SECONDS

    def test_custom_config(self):
        """Test creating config with custom values."""
        config = Config(
            width=32,
            height=24,
            x_offset=5,
            y_offset=10,
            host="192.168.1.100",
            port=5000,
            frame_delay_ms=16,
            timeout_seconds=10,
        )

        assert config.width == 32
        assert config.height == 24
        assert config.x_offset == 5
        assert config.y_offset == 10
        assert config.host == "192.168.1.100"
        assert config.port == 5000
        assert config.frame_delay_ms == 16
        assert config.timeout_seconds == 10

    def test_validate_valid_config(self):
        """Test validation with valid config."""
        config = Config(width=45, height=35, host="localhost", port=1337)

        # Should not raise
        config.validate()

    def test_validate_invalid_width(self):
        """Test validation with invalid width."""
        config = Config(width=0)

        with pytest.raises(ValueError, match="Width and height must be positive"):
            config.validate()

    def test_validate_invalid_height(self):
        """Test validation with invalid height."""
        config = Config(height=-1)

        with pytest.raises(ValueError, match="Width and height must be positive"):
            config.validate()

    def test_validate_empty_host(self):
        """Test validation with empty host."""
        config = Config(host="")

        with pytest.raises(ValueError, match="Host cannot be empty"):
            config.validate()

    def test_validate_invalid_port_low(self):
        """Test validation with port too low."""
        config = Config(port=0)

        with pytest.raises(ValueError, match="Port must be between"):
            config.validate()

    def test_validate_invalid_port_high(self):
        """Test validation with port too high."""
        config = Config(port=70000)

        with pytest.raises(ValueError, match="Port must be between"):
            config.validate()

    def test_validate_negative_frame_delay(self):
        """Test validation with negative frame delay."""
        config = Config(frame_delay_ms=-1)

        with pytest.raises(ValueError, match="Frame delay cannot be negative"):
            config.validate()

    def test_validate_negative_timeout(self):
        """Test validation with negative timeout."""
        config = Config(timeout_seconds=-5)

        with pytest.raises(ValueError, match="Timeout cannot be negative"):
            config.validate()

    def test_repr(self):
        """Test string representation."""
        config = Config(width=32, height=24, x_offset=5, y_offset=10, host="test.local", port=2000)

        repr_str = repr(config)

        assert "width=32" in repr_str
        assert "height=24" in repr_str
        assert "test.local:2000" in repr_str

    def test_layer_constants(self):
        """Test layer boundary constants."""
        assert Config.MIN_LAYER == 0
        assert Config.MAX_LAYER == 15


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
