"""Canvas abstraction for pixel rendering and frame management."""

import os
import socket
import time
from typing import Optional

from flaschen_taschen.client.color import Color
from flaschen_taschen.client.config import Config
from flaschen_taschen.client.ppm_formatter import PPMFormatter
from flaschen_taschen.client.udp_client import DisplayConnection


def _get_max_udp_size() -> int:
    """Get the maximum UDP datagram size for this system.

    Priority:
    1. FT_UDP_SIZE environment variable (if set)
    2. System SO_SNDBUF socket option (actual system limit)
    3. Default fallback (65507)
    """
    # Check environment variable first
    if 'FT_UDP_SIZE' in os.environ:
        return int(os.environ['FT_UDP_SIZE'])

    # Try to query system UDP limit via socket option
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udp_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            return udp_size
        finally:
            s.close()
    except Exception:
        pass

    # Fallback default
    return 65507


class Canvas:
    """Abstract canvas for pixel manipulation with multi-layer support and frame buffering."""

    def __init__(self, config: Optional[Config] = None, auto_send: bool = True):
        """Initialize canvas.

        Args:
            config: Config object with display geometry and settings
            auto_send: If True, automatically send frames after draw() and explicit send()
        """
        self.config = config or Config()
        self.config.validate()

        self.auto_send = auto_send
        self.connection = DisplayConnection(self.config)

        # Initialize pixel buffer (RGBA for compositing)
        # Stored as pixels[y][x] = (r, g, b, a)
        self.pixels = [
            [(0, 0, 0, 255) for _ in range(self.config.width)]
            for _ in range(self.config.height)
        ]

        # Track if pixels have been modified
        self.dirty = True

        # Frame timing
        self._frame_count = 0
        self._start_time = time.time()

    @property
    def width(self) -> int:
        """Get canvas width."""
        return self.config.width

    @property
    def height(self) -> int:
        """Get canvas height."""
        return self.config.height

    def set_pixel(self, x: int, y: int, color: Color):
        """Set a single pixel.

        Args:
            x: X coordinate
            y: Y coordinate
            color: Color to set
        """
        if 0 <= x < self.config.width and 0 <= y < self.config.height:
            self.pixels[y][x] = (color.r, color.g, color.b, 255)
            self.dirty = True

    def get_pixel(self, x: int, y: int) -> Optional[Color]:
        """Get a single pixel color.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Color at (x, y) or None if out of bounds
        """
        if 0 <= x < self.config.width and 0 <= y < self.config.height:
            r, g, b, _ = self.pixels[y][x]
            return Color(r, g, b)
        return None

    def clear(self, color: Optional[Color] = None):
        """Clear the canvas with a color.

        Args:
            color: Color to fill with (default: black)
        """
        if color is None:
            color = Color.BLACK

        for y in range(self.config.height):
            for x in range(self.config.width):
                self.pixels[y][x] = (color.r, color.g, color.b, 255)

        self.dirty = True

    def fill(self, color: Color):
        """Fill the entire canvas with a color.

        Args:
            color: Color to fill with
        """
        for y in range(self.config.height):
            for x in range(self.config.width):
                self.pixels[y][x] = (color.r, color.g, color.b, 255)

        self.dirty = True

    def fill_rect(self, x: int, y: int, width: int, height: int, color: Color):
        """Fill a rectangle with a color.

        Args:
            x: Left X coordinate
            y: Top Y coordinate
            width: Rectangle width
            height: Rectangle height
            color: Fill color
        """
        for dy in range(height):
            for dx in range(width):
                self.set_pixel(x + dx, y + dy, color)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: Color):
        """Draw a line using Bresenham's algorithm.

        Args:
            x1, y1: Start point
            x2, y2: End point
            color: Line color
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x2 > x1 else -1
        sy = 1 if y2 > y1 else -1

        if dx > dy:
            err = dx / 2
            y = y1
            for x in range(x1, x2 + sx, sx):
                self.set_pixel(x, y, color)
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
        else:
            err = dy / 2
            x = x1
            for y in range(y1, y2 + sy, sy):
                self.set_pixel(x, y, color)
                err -= dx
                if err < 0:
                    x += sx
                    err += dy

    def draw_circle(self, cx: int, cy: int, radius: int, color: Color, filled: bool = False):
        """Draw a circle using Midpoint Circle Algorithm.

        Args:
            cx, cy: Center point
            radius: Circle radius
            color: Circle color
            filled: If True, fill the circle
        """
        x = 0
        y = radius
        d = 3 - 2 * radius

        while x <= y:
            if filled:
                # Draw horizontal lines for filled circle
                self.draw_line(cx - x, cy - y, cx + x, cy - y, color)
                self.draw_line(cx - x, cy + y, cx + x, cy + y, color)
                self.draw_line(cx - y, cy - x, cx + y, cy - x, color)
                self.draw_line(cx - y, cy + x, cx + y, cy + x, color)
            else:
                # Draw circle outline
                self.set_pixel(cx + x, cy + y, color)
                self.set_pixel(cx - x, cy + y, color)
                self.set_pixel(cx + x, cy - y, color)
                self.set_pixel(cx - x, cy - y, color)
                self.set_pixel(cx + y, cy + x, color)
                self.set_pixel(cx - y, cy + x, color)
                self.set_pixel(cx + y, cy - x, color)
                self.set_pixel(cx - y, cy - x, color)

            if d < 0:
                d = d + 4 * x + 6
            else:
                d = d + 4 * (x - y) + 10
                y -= 1

            x += 1

    def send(self, force: bool = False) -> bool:
        """Send current frame to display.

        Args:
            force: If True, send immediately without rate limiting

        Returns:
            True if sent successfully
        """
        # Convert RGBA pixels to RGB tuples for PPM encoding
        rgb_pixels = []
        for row in self.pixels:
            rgb_row = [(r, g, b) for r, g, b, _ in row]
            rgb_pixels.append(rgb_row)

        # Send in multiple packets if needed (like C++ implementation)
        # This ensures the header with layer metadata is properly sent for each tile
        success = self._send_tiled(rgb_pixels, force=force)

        if success:
            self._frame_count += 1
            self.dirty = False

        return success

    def _send_tiled(self, rgb_pixels: list, force: bool = False) -> bool:
        """Send pixels in tiles, matching C++ implementation behavior.

        The C++ UDP client splits large images into multiple packets,
        with each packet containing its own PPM header (including layer metadata).
        This ensures the display server correctly receives the layer information.

        Args:
            rgb_pixels: 2D list of (r, g, b) tuples
            force: If True, send immediately without rate limiting

        Returns:
            True if all packets sent successfully
        """
        # Calculate how many rows fit in a single UDP packet
        # Reserve 64 bytes for header (matching C++ kFlaschenTaschenHeaderReserve)
        max_udp_size = _get_max_udp_size()
        header_reserve = 64
        row_size = 3 * self.config.width
        max_rows_per_packet = (max_udp_size - header_reserve) // row_size

        if max_rows_per_packet <= 0:
            max_rows_per_packet = 1

        height = len(rgb_pixels)
        tile_offset = 0
        all_success = True

        # Send each tile as a separate packet with its own header
        while tile_offset < height:
            send_height = min(max_rows_per_packet, height - tile_offset)

            # Extract this tile's rows
            tile_pixels = rgb_pixels[tile_offset:tile_offset + send_height]

            # Encode tile with proper header containing layer metadata
            # Note: y_offset is adjusted for each tile, but layer stays constant
            ppm_data = PPMFormatter.encode(
                tile_pixels,
                x_offset=self.config.x_offset,
                y_offset=self.config.y_offset + tile_offset,
                layer=self.config.layer,
            )

            # Send this tile's packet
            success = self.connection.send_frame(ppm_data, force=force)
            if not success:
                all_success = False

            tile_offset += send_height

        return all_success

    def draw(self):
        """Draw the current frame (placeholder for user implementation).

        This is typically overridden in subclasses or called after
        pixel operations. If auto_send is enabled, send() is called
        automatically.
        """
        if self.auto_send:
            self.send()

    def flush(self):
        """Ensure all pending frames are sent."""
        if self.dirty:
            self.send()

    def get_frame_info(self) -> dict:
        """Get frame statistics.

        Returns:
            Dictionary with:
            - frame_count: Total frames sent
            - elapsed_time: Seconds since creation
            - fps: Frames per second
        """
        elapsed = time.time() - self._start_time
        fps = self._frame_count / elapsed if elapsed > 0 else 0
        return {
            "frame_count": self._frame_count,
            "elapsed_time": elapsed,
            "fps": fps,
        }

    def close(self):
        """Close canvas and connection."""
        self.flush()
        self.connection.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.close()
        except:
            pass


class LayeredCanvas:
    """Canvas with explicit multi-layer support (0-15 layers)."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize layered canvas.

        Args:
            config: Config object with display geometry
        """
        self.config = config or Config()
        self.config.validate()

        self.connection = DisplayConnection(self.config)

        # Create separate canvas for each layer
        self.layers = {}
        for layer_num in range(self.config.MAX_LAYER + 1):
            self.layers[layer_num] = [
                [(0, 0, 0, 0) for _ in range(self.config.width)]
                for _ in range(self.config.height)
            ]

        self._frame_count = 0

    def get_layer_canvas(self, layer: int) -> Canvas:
        """Get or create a canvas for a specific layer.

        Args:
            layer: Layer number (0-15)

        Returns:
            Canvas object bound to this layer
        """
        if not (self.config.MIN_LAYER <= layer <= self.config.MAX_LAYER):
            raise ValueError(f"Layer must be between {self.config.MIN_LAYER} and {self.config.MAX_LAYER}")

        # For now, return a basic canvas
        # In full implementation, would track layer state
        canvas = Canvas(self.config, auto_send=False)
        canvas.layer = layer
        return canvas

    def send_layer(self, layer: int, pixels: list) -> bool:
        """Send a specific layer.

        Args:
            layer: Layer number (0-15)
            pixels: 2D pixel list

        Returns:
            True if sent successfully
        """
        rgb_pixels = [[(r, g, b) for r, g, b, _ in row] for row in pixels]

        # Calculate how many rows fit in a single UDP packet (matching C++ behavior)
        max_udp_size = _get_max_udp_size()
        header_reserve = 64
        row_size = 3 * self.config.width
        max_rows_per_packet = (max_udp_size - header_reserve) // row_size

        if max_rows_per_packet <= 0:
            max_rows_per_packet = 1

        height = len(rgb_pixels)
        tile_offset = 0
        all_success = True

        # Send each tile as a separate packet with its own header
        while tile_offset < height:
            send_height = min(max_rows_per_packet, height - tile_offset)

            # Extract this tile's rows
            tile_pixels = rgb_pixels[tile_offset:tile_offset + send_height]

            # Encode tile with proper header containing layer metadata
            ppm_data = PPMFormatter.encode(
                tile_pixels,
                x_offset=self.config.x_offset,
                y_offset=self.config.y_offset + tile_offset,
                layer=layer,
            )

            # Send this tile's packet
            success = self.connection.send_frame(ppm_data)
            if not success:
                all_success = False

            tile_offset += send_height

        return all_success

    def close(self):
        """Close all layers."""
        self.connection.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
