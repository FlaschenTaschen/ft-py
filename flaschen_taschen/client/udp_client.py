"""UDP socket communication for sending frames to the display."""

import socket
import time
from typing import Optional

from flaschen_taschen.client.config import Config


class UDPClient:
    """UDP client for communicating with FlaschenTaschen display server."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize UDP client.

        Args:
            config: Config object with host, port, and timeout settings.
                   If None, creates default Config.
        """
        self.config = config or Config()
        self.config.validate()

        self.socket: Optional[socket.socket] = None
        self._connect()

    def _connect(self):
        """Establish UDP socket connection."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(self.config.timeout_seconds)
        except OSError as e:
            raise RuntimeError(f"Failed to create UDP socket: {e}")

    def send_data(self, data: bytes) -> bool:
        """Send raw data to display.

        Args:
            data: Bytes to send

        Returns:
            True if sent successfully, False otherwise
        """
        if self.socket is None:
            raise RuntimeError("Socket not connected")

        try:
            self.socket.sendto(data, (self.config.host, self.config.port))
            return True
        except (OSError, socket.timeout) as e:
            print(f"Failed to send data: {e}")
            return False

    def close(self):
        """Close UDP socket connection."""
        if self.socket:
            try:
                self.socket.close()
            except OSError:
                pass
            self.socket = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __del__(self):
        """Cleanup on deletion."""
        self.close()


class DisplayConnection:
    """High-level display connection wrapper with automatic reconnection."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize display connection.

        Args:
            config: Config object for connection settings
        """
        self.config = config or Config()
        self.client = UDPClient(self.config)
        self._last_send_time = 0

    def send_frame(self, data: bytes, force=False) -> bool:
        """Send a frame with rate limiting.

        Args:
            data: Frame data bytes
            force: If True, send immediately without rate limiting

        Returns:
            True if sent successfully
        """
        if not force:
            # Apply frame rate limiting
            elapsed = time.time() - self._last_send_time
            delay_needed = self.config.frame_delay_ms / 1000.0
            if elapsed < delay_needed:
                time.sleep(delay_needed - elapsed)

        success = self.client.send_data(data)
        if success:
            self._last_send_time = time.time()
        return success

    def close(self):
        """Close connection."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
