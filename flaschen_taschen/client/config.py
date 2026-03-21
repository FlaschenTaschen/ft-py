"""Configuration module for display geometry and connection settings."""


class Config:
    """Stores display configuration including geometry and connection parameters."""

    # Default display geometry (45x35 pixels)
    DEFAULT_WIDTH = 45
    DEFAULT_HEIGHT = 35
    DEFAULT_X_OFFSET = 0
    DEFAULT_Y_OFFSET = 0

    # Default connection settings
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 1337

    # Timing settings
    DEFAULT_FRAME_DELAY_MS = 33  # ~30 FPS
    DEFAULT_TIMEOUT_SECONDS = 5

    # Layer management
    MIN_LAYER = 0
    MAX_LAYER = 15

    def __init__(
        self,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        x_offset=DEFAULT_X_OFFSET,
        y_offset=DEFAULT_Y_OFFSET,
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        frame_delay_ms=DEFAULT_FRAME_DELAY_MS,
        timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
        layer=0,
    ):
        """Initialize configuration.

        Args:
            width: Display width in pixels (default: 45)
            height: Display height in pixels (default: 35)
            x_offset: X offset for layer placement (default: 0)
            y_offset: Y offset for layer placement (default: 0)
            host: Display hostname/IP (default: "localhost")
            port: UDP port (default: 1337)
            frame_delay_ms: Delay between frames in milliseconds (default: 33)
            timeout_seconds: Socket timeout in seconds (default: 5)
            layer: Layer 0-15 for display stacking (default: 0)
        """
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.host = host
        self.port = port
        self.frame_delay_ms = frame_delay_ms
        self.timeout_seconds = timeout_seconds
        self.layer = layer

    def validate(self):
        """Validate configuration values.

        Raises:
            ValueError: If any configuration is invalid
        """
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"Width and height must be positive: {self.width}x{self.height}")
        if not self.host:
            raise ValueError("Host cannot be empty")
        if self.port <= 0 or self.port > 65535:
            raise ValueError(f"Port must be between 1 and 65535: {self.port}")
        if self.frame_delay_ms < 0:
            raise ValueError(f"Frame delay cannot be negative: {self.frame_delay_ms}")
        if self.timeout_seconds < 0:
            raise ValueError(f"Timeout cannot be negative: {self.timeout_seconds}")

    def __repr__(self):
        return (
            f"Config(width={self.width}, height={self.height}, "
            f"offset=({self.x_offset},{self.y_offset}), "
            f"host={self.host}:{self.port})"
        )
