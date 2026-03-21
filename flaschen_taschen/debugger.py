"""Simple debugger for FlaschenTaschen displays - cycles through colors."""

import asyncio
import time
from enum import Enum
from typing import Optional

from .client.canvas import Canvas
from .client.color import Color, create_hsv_palette
from .client.config import Config


class Mode(Enum):
    """Debugger display modes."""
    EDGES = "edges"
    FILL = "fill"


class DisplayDebugger:
    """Simple debugger that cycles through colors while drawing edges or filling display."""

    def __init__(
        self,
        mode: Mode = Mode.EDGES,
        palette: Optional[list[Color]] = None,
        config: Optional[Config] = None,
    ):
        """Initialize debugger.

        Args:
            mode: Display mode (edges or fill)
            palette: List of Color objects to cycle through
            config: Display configuration
        """
        self.mode = mode
        self.config = config or Config()
        self.canvas = Canvas(self.config, auto_send=False)

        # Default to rainbow palette if none provided
        if palette is None:
            palette = create_hsv_palette(256).colors
        self.palette = palette

    def draw_edges(self, color: Color) -> None:
        """Draw colored edge outline."""
        self.canvas.clear()
        width = self.config.width
        height = self.config.height

        # Top and bottom edges
        for x in range(width):
            self.canvas.set_pixel(x, 0, color)
            self.canvas.set_pixel(x, height - 1, color)

        # Left and right edges
        for y in range(1, height - 1):
            self.canvas.set_pixel(0, y, color)
            self.canvas.set_pixel(width - 1, y, color)

    def draw_fill(self, color: Color) -> None:
        """Fill entire display with color."""
        self.canvas.clear()
        width = self.config.width
        height = self.config.height

        for x in range(width):
            for y in range(height):
                self.canvas.set_pixel(x, y, color)

    def run(self, timeout: float = 10.0, delay_ms: int = 0) -> None:
        """Run debugger animation cycling through palette colors.

        Args:
            timeout: How long to run in seconds
            delay_ms: Delay between frames in milliseconds
        """
        start_time = time.time()
        color_index = 0
        frame_count = 0

        while time.time() - start_time < timeout:
            color = self.palette[color_index % len(self.palette)]

            # Draw appropriate mode
            if self.mode == Mode.EDGES:
                self.draw_edges(color)
            else:  # FILL
                self.draw_fill(color)

            # Send frame
            self.canvas.send()
            frame_count += 1

            # Log every 30 frames
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                print(f"Frame {frame_count} at {elapsed:.1f}s, color_index={color_index}")

            # Move to next color
            color_index += 1

            # Frame rate control
            if delay_ms > 0:
                time.sleep(delay_ms / 1000.0)

        print(f"Done. Sent {frame_count} frames in {timeout}s")
