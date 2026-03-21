"""Video generator - stream video frames to FlaschenTaschen display."""

import subprocess
import sys
import time
from io import BytesIO
from flaschen_taschen.client.canvas import Canvas
from flaschen_taschen.client.color import Color

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


class VideoGenerator:
    """Stream video frames to FlaschenTaschen display."""

    def __init__(self, canvas, video_path, frame_rate=30):
        """
        Initialize video generator.

        Args:
            canvas: Canvas object to draw on
            video_path: Path to video file
            frame_rate: Target frame rate for playback
        """
        self.canvas = canvas
        self.video_path = video_path
        self.frame_rate = max(1, frame_rate)
        self.frame_delay = 1.0 / self.frame_rate

    def _extract_frames_ffmpeg(self):
        """
        Extract video frames using ffmpeg subprocess.

        Yields:
            PIL Image objects for each frame
        """
        if not HAS_PILLOW:
            raise RuntimeError(
                "Pillow not installed. Install with: pip install pillow"
            )

        # Use ffmpeg to extract frames as PPM format (fast binary output)
        cmd = [
            'ffmpeg',
            '-loglevel', 'error',  # Suppress progress output
            '-i', self.video_path,
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vf', f'scale={self.canvas.width}:{self.canvas.height}:force_original_aspect_ratio=decrease',
            '-vcodec', 'ppm',
            '-',
        ]

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1024 * 1024,  # 1MB buffer
            )
        except FileNotFoundError:
            raise RuntimeError(
                "ffmpeg not found. Install with: sudo apt-get install ffmpeg (Linux/RPi) "
                "or brew install ffmpeg (macOS)"
            )

        try:
            while True:
                # Read PPM header
                header_lines = []
                width = height = 0

                # Read first few bytes to get magic number
                magic = proc.stdout.read(3)
                if not magic.startswith(b'P6'):
                    break

                # Read header lines until we have width, height, and max_value
                for _ in range(10):  # Max 10 lines to prevent infinite loop
                    line = b''
                    while True:
                        byte = proc.stdout.read(1)
                        if not byte:
                            break
                        if byte == b'\n':
                            break
                        if byte != b'\r':
                            line += byte

                    if not line:
                        break

                    line_str = line.decode('ascii', errors='ignore').strip()

                    # Skip comments and empty lines
                    if not line_str or line_str.startswith('#'):
                        continue

                    # Parse dimensions
                    try:
                        parts = line_str.split()
                        if len(parts) >= 2:
                            width, height = int(parts[0]), int(parts[1])
                            header_lines.append(line_str)
                        elif len(parts) == 1:
                            if width == 0:
                                width = int(parts[0])
                            else:
                                # This is max_value, we're done with header
                                header_lines.append(line_str)
                                break
                            header_lines.append(line_str)
                    except ValueError:
                        continue

                if width <= 0 or height <= 0:
                    break

                # Read pixel data
                frame_size = width * height * 3
                pixel_data = proc.stdout.read(frame_size)

                if len(pixel_data) < frame_size:
                    break

                # Create image from pixel data
                img = Image.frombytes('RGB', (width, height), pixel_data)
                yield img

        finally:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()

    def render(self, duration=None, x_offset=0, y_offset=0):
        """
        Render video to canvas, looping until duration expires.

        Args:
            duration: Duration in seconds (None = loop indefinitely)
            x_offset: X offset on canvas
            y_offset: Y offset on canvas
        """
        if not HAS_PILLOW:
            raise RuntimeError(
                "Pillow not installed. Install with: pip install pillow"
            )

        start_time = time.time()
        frame_count = 0

        # Loop video continuously
        while True:
            # Check duration limit
            if duration:
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break

            for frame in self._extract_frames_ffmpeg():
                # Check duration limit again inside frame loop
                if duration:
                    elapsed = time.time() - start_time
                    if elapsed >= duration:
                        return

                # Ensure frame fits on canvas
                if frame.width != self.canvas.width - x_offset or frame.height != self.canvas.height - y_offset:
                    # Resize frame if needed
                    frame = frame.resize(
                        (self.canvas.width - x_offset, self.canvas.height - y_offset),
                        Image.LANCZOS
                    )

                # Draw frame to canvas
                pixels = frame.load()
                for y in range(frame.height):
                    for x in range(frame.width):
                        pixel = pixels[x, y]
                        if isinstance(pixel, (tuple, list)):
                            r, g, b = pixel[:3]
                        else:
                            r = g = b = pixel
                        color = Color(r, g, b)
                        self.canvas.set_pixel(x + x_offset, y + y_offset, color)

                self.canvas.send()

                # Frame rate control
                frame_count += 1
                frame_time = (time.time() - start_time) / frame_count
                if frame_time < self.frame_delay:
                    time.sleep(self.frame_delay - frame_time)


def send_video(host, port, geometry, video_path, layer=0, delay_ms=0, timeout_s=10, duration_s=None, frame_rate=30):
    """
    Convenience function to stream video to display.

    Args:
        host: Hostname/IP
        port: Port number
        geometry: Tuple (width, height, x_offset, y_offset)
        video_path: Path to video file
        layer: Layer number (0-15)
        delay_ms: Frame delay in milliseconds
        timeout_s: Connection timeout in seconds
        duration_s: Video playback duration in seconds
        frame_rate: Target frame rate
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
    generator = VideoGenerator(canvas, video_path, frame_rate=frame_rate)
    generator.render(
        duration=duration_s or timeout_s,
        x_offset=config.x_offset,
        y_offset=config.y_offset,
    )
