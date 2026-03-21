"""Image generator - load and display images on FlaschenTaschen."""

import sys
import time
from flaschen_taschen.client.canvas import Canvas
from flaschen_taschen.client.color import Color

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


class ImageGenerator:
    """Load and render images to FlaschenTaschen display."""

    def __init__(self, canvas, image_data=None, image_path=None):
        """
        Initialize image generator.

        Args:
            canvas: Canvas object to draw on
            image_data: PIL Image object (or numpy array)
            image_path: Path to image file (requires Pillow)
        """
        self.canvas = canvas
        self.image = None

        if image_data is not None:
            self.image = image_data
        elif image_path is not None:
            if not HAS_PILLOW:
                raise RuntimeError(
                    "Pillow not installed. Install with: pip install pillow"
                )
            self.image = Image.open(image_path)
        else:
            raise ValueError("Either image_data or image_path required")

    def _resize_image(self, img, width, height):
        """Resize image to canvas dimensions using nearest-neighbor."""
        if not HAS_PILLOW:
            raise RuntimeError("Pillow required for image resizing")

        # Use LANCZOS for good quality downscaling, NEAREST for upscaling
        if img.width > width or img.height > height:
            resample = Image.LANCZOS
        else:
            resample = Image.NEAREST

        return img.resize((width, height), resample)

    def _quantize_color(self, pixel):
        """Convert pixel to RGB tuple, clamping to valid range."""
        if isinstance(pixel, (tuple, list)):
            # Already a color tuple
            r, g, b = pixel[:3]
        elif isinstance(pixel, int):
            # Grayscale
            r = g = b = pixel
        else:
            # Fallback to black
            r = g = b = 0

        return (
            max(0, min(255, int(r))),
            max(0, min(255, int(g))),
            max(0, min(255, int(b))),
        )

    def render(self, x_offset=0, y_offset=0, duration=None):
        """
        Render image to canvas.

        For animated images (e.g., GIFs), loops and renders all frames with proper timing.
        For static images, renders a single frame.

        Args:
            x_offset: X offset on canvas
            y_offset: Y offset on canvas
            duration: Duration in seconds to loop animation (None = loop indefinitely)
        """
        if self.image is None:
            raise ValueError("No image loaded")

        if not HAS_PILLOW:
            raise RuntimeError(
                "Pillow not installed. Install with: pip install pillow"
            )

        # Check if this is an animated image
        is_animated = hasattr(self.image, 'n_frames') and self.image.n_frames > 1
        num_frames = self.image.n_frames if is_animated else 1

        # For static images, just render once
        if not is_animated:
            self._render_frame(0, x_offset, y_offset)
            return

        # For animated images, loop until duration expires
        start_time = time.time()
        frame_idx = 0

        while True:
            self.image.seek(frame_idx)
            self._render_frame(frame_idx, x_offset, y_offset)

            # Check if we've exceeded the duration
            if duration is not None:
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break

            # Move to next frame
            frame_idx = (frame_idx + 1) % num_frames

            # Respect frame duration from GIF metadata
            frame_duration_ms = self.image.info.get('duration', 100)
            time.sleep(frame_duration_ms / 1000.0)

    def _render_frame(self, frame_idx, x_offset, y_offset):
        """Render a single frame to canvas.

        Args:
            frame_idx: Frame index (for logging/debugging)
            x_offset: X offset on canvas
            y_offset: Y offset on canvas
        """
        # Clear canvas before drawing each frame
        self.canvas.clear()

        img = self.image

        # Convert RGBA to RGB
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Resize to canvas dimensions
        target_width = self.canvas.width - x_offset
        target_height = self.canvas.height - y_offset

        if target_width <= 0 or target_height <= 0:
            # Image offset is beyond canvas
            self.canvas.send()
            return

        img = self._resize_image(img, target_width, target_height)

        # Draw pixels to canvas
        pixels = img.load()
        for y in range(img.height):
            for x in range(img.width):
                pixel = pixels[x, y]
                r, g, b = self._quantize_color(pixel)
                color = Color(r, g, b)
                self.canvas.set_pixel(x + x_offset, y + y_offset, color)

        self.canvas.send()


def send_image(host, port, geometry, image_path, layer=0, delay_ms=0, timeout_s=10):
    """
    Convenience function to send image to display.

    Args:
        host: Hostname/IP
        port: Port number
        geometry: Tuple (width, height, x_offset, y_offset)
        image_path: Path to image file
        layer: Layer number (0-15)
        delay_ms: Frame delay in milliseconds
        timeout_s: Connection timeout in seconds
    """
    from flaschen_taschen.client.udp_client import DisplayConnection
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
    generator = ImageGenerator(canvas, image_path=image_path)
    generator.render(
        x_offset=config.x_offset,
        y_offset=config.y_offset,
        duration=timeout_s,
    )
