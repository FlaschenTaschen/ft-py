"""Text generator - render text with BDF fonts to display."""

import os
import sys
import time
from flaschen_taschen.client.canvas import Canvas
from flaschen_taschen.client.color import Color
from flaschen_taschen.utils.bdf_font import BDFFont


class TextGenerator:
    """Generate text on FlaschenTaschen display using BDF fonts."""

    def __init__(self, canvas, text, font_path, color=None, scroll=True, scroll_speed=1):
        """
        Initialize text generator.

        Args:
            canvas: Canvas object to draw on
            text: Text to display
            font_path: Path to .bdf font file
            color: Color for text (default: white)
            scroll: Enable scrolling text
            scroll_speed: Scroll speed in pixels per frame
        """
        self.canvas = canvas
        self.text = text
        self.font = BDFFont(font_path)
        self.color = color or Color.WHITE
        self.scroll = scroll
        self.scroll_speed = scroll_speed

    def render_static(self, x=0, y=0):
        """
        Render static (non-scrolling) text at given position.

        Args:
            x: X position
            y: Y position
        """
        self.canvas.clear()
        current_x = x

        for char in self.text:
            char_bitmap = self.font.render_char(char)
            if char_bitmap is None:
                continue

            char_width = self.font.get_char_width(char)
            char_height = self.font.get_char_height()

            # Draw character pixels
            for row_idx, row in enumerate(char_bitmap):
                for col_idx, pixel in enumerate(row):
                    if pixel:
                        px = current_x + col_idx
                        py = y + row_idx
                        if 0 <= px < self.canvas.width and 0 <= py < self.canvas.height:
                            self.canvas.set_pixel(px, py, self.color)

            current_x += char_width

    def render_scrolling(self, y=None, duration=None, frame_rate=30):
        """
        Render scrolling text that moves across display.

        Args:
            y: Y position to scroll text
            duration: Duration in seconds (None = scroll once across display)
            frame_rate: Frame rate for animation
        """
        if y is None:
            y = (self.canvas.height - self.font.get_text_height()) // 2

        text_width = self.font.get_text_width(self.text)
        frame_delay = 1.0 / frame_rate

        # Calculate scrolling range
        start_x = self.canvas.width
        end_x = -text_width

        if duration:
            # Calculate pixels per frame to complete in duration
            total_pixels = start_x - end_x
            frames = int(duration * frame_rate)
            pixels_per_frame = total_pixels / frames if frames > 0 else 1
        else:
            pixels_per_frame = self.scroll_speed

        x_pos = start_x
        start_time = time.time()

        while True:
            self.canvas.clear()

            # Draw text at current position
            current_x = int(x_pos)

            for char in self.text:
                char_bitmap = self.font.render_char(char)
                if char_bitmap is None:
                    continue

                char_width = self.font.get_char_width(char)

                # Draw character pixels
                for row_idx, row in enumerate(char_bitmap):
                    for col_idx, pixel in enumerate(row):
                        if pixel:
                            px = current_x + col_idx
                            py = y + row_idx
                            if 0 <= px < self.canvas.width and 0 <= py < self.canvas.height:
                                self.canvas.set_pixel(px, py, self.color)

                current_x += char_width

            self.canvas.send()

            # Check if animation is complete
            if x_pos <= end_x:
                break

            if duration:
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break

            # Move for next frame
            x_pos -= pixels_per_frame
            time.sleep(frame_delay)

    def render(self, x=0, y=None, duration=None, frame_rate=30):
        """
        Render text (static or scrolling based on settings).

        Args:
            x: X position (used for static text)
            y: Y position
            duration: Duration in seconds (for scrolling)
            frame_rate: Frame rate for scrolling animation
        """
        if self.scroll:
            self.render_scrolling(y=y, duration=duration, frame_rate=frame_rate)
        else:
            self.render_static(x=x, y=y or 0)
            self.canvas.send()


def send_text(host, port, geometry, text, font_path, color=None, layer=0, delay_ms=0, timeout_s=10, scroll=True):
    """
    Convenience function to send text to display.

    Args:
        host: Hostname/IP
        port: Port number
        geometry: Tuple (width, height, x_offset, y_offset)
        text: Text to display
        font_path: Path to .bdf font file
        color: Color object (default: white)
        layer: Layer number (0-15)
        delay_ms: Frame delay in milliseconds
        timeout_s: Connection timeout in seconds
        scroll: Enable scrolling
    """
    from flaschen_taschen.client.config import Config

    config = Config(
        width=geometry[0],
        height=geometry[1],
        x_offset=geometry[2] if len(geometry) > 2 else 0,
        y_offset=geometry[3] if len(geometry) > 3 else 0,
        host=host,
        port=port,
        frame_delay_ms=delay_ms,
        timeout_seconds=timeout_s,
    )

    canvas = Canvas(config)
    generator = TextGenerator(canvas, text, font_path, color=color, scroll=scroll)
    generator.render(duration=timeout_s)
