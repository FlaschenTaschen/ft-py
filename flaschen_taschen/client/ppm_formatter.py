"""PPM binary format encoder and decoder with FlaschenTaschen metadata extensions."""

import struct
from typing import List, Optional, Tuple

from flaschen_taschen.client.color import Color


class PPMFormatter:
    """Encodes and decodes PPM (P6) format with FT metadata extensions."""

    # PPM magic number for binary format
    PPM_MAGIC = b"P6"
    MAX_COLOR_VALUE = 255

    @classmethod
    def encode(
        cls,
        pixels: List[List[Tuple[int, int, int]]],
        x_offset: int = 0,
        y_offset: int = 0,
        layer: int = 0,
    ) -> bytes:
        """Encode pixel data to PPM binary format with FT metadata.

        Args:
            pixels: 2D list of (r, g, b) tuples indexed as pixels[y][x]
            x_offset: X offset for layer placement
            y_offset: Y offset for layer placement
            layer: Layer number (0-15)

        Returns:
            PPM binary data with FT metadata header
        """
        if not pixels or not pixels[0]:
            raise ValueError("Pixel data cannot be empty")

        height = len(pixels)
        width = len(pixels[0])

        # Validate pixel data format
        for row in pixels:
            if len(row) != width:
                raise ValueError("All pixel rows must have same width")

        # Build PPM header with FT metadata (order matters!)
        header = cls.PPM_MAGIC + b"\n"

        # PPM image dimensions (must come before FT metadata)
        dimensions = f"{width} {height}\n"
        header += dimensions.encode("ascii")

        # FT metadata comment: #FT: <x> <y> <layer>
        ft_metadata = f"#FT: {x_offset} {y_offset} {layer}\n"
        header += ft_metadata.encode("ascii")

        # Max color value
        max_color = f"{cls.MAX_COLOR_VALUE}\n"
        header += max_color.encode("ascii")

        # Encode pixel data in binary format (P6)
        # Each pixel is 3 bytes: R, G, B
        pixel_data = b""
        for row in pixels:
            for r, g, b in row:
                # Clamp values to 0-255
                r = max(0, min(255, int(r)))
                g = max(0, min(255, int(g)))
                b = max(0, min(255, int(b)))
                pixel_data += struct.pack("BBB", r, g, b)

        return header + pixel_data

    @classmethod
    def decode(cls, data: bytes) -> dict:
        """Decode PPM binary format with FT metadata.

        Args:
            data: PPM binary data

        Returns:
            Dictionary with keys:
            - 'pixels': 2D list of (r, g, b) tuples
            - 'width': Image width
            - 'height': Image height
            - 'x_offset': X offset (from FT metadata)
            - 'y_offset': Y offset (from FT metadata)
            - 'layer': Layer number (from FT metadata)
        """
        # Read magic number
        if not data.startswith(b"P6"):
            raise ValueError("Invalid PPM format: must be P6")

        # Split header from pixel data at first binary marker
        # We need to read: magic, then skip comments/whitespace, read width/height/maxval
        lines_data = b""
        pos = 2  # Skip "P6"

        ft_data = {"x_offset": 0, "y_offset": 0, "layer": 0}
        header_complete = False
        header_lines_count = 0

        # Parse header line by line
        while pos < len(data) and not header_complete:
            # Skip whitespace
            while pos < len(data) and data[pos : pos + 1] in (b" ", b"\t", b"\n", b"\r"):
                pos += 1

            if pos >= len(data):
                break

            # Read next line
            line_start = pos
            while pos < len(data) and data[pos : pos + 1] not in (b"\n", b"\r"):
                pos += 1

            line = data[line_start:pos]
            if pos < len(data) and data[pos : pos + 1] in (b"\n", b"\r"):
                pos += 1

            # Handle comments
            if line.startswith(b"#"):
                if line.startswith(b"#FT:"):
                    try:
                        parts = line[4:].decode("ascii").split()
                        ft_data = {
                            "x_offset": int(parts[0]) if len(parts) > 0 else 0,
                            "y_offset": int(parts[1]) if len(parts) > 1 else 0,
                            "layer": int(parts[2]) if len(parts) > 2 else 0,
                        }
                    except (IndexError, ValueError):
                        pass
                continue

            # Count non-comment header lines
            if line and not line.startswith(b"#"):
                header_lines_count += 1
                if header_lines_count == 1:
                    # Parse width and height
                    try:
                        width, height = map(int, line.split())
                    except ValueError:
                        raise ValueError("Invalid PPM header: cannot parse dimensions")
                elif header_lines_count == 2:
                    # Parse max color value
                    try:
                        max_color = int(line)
                    except ValueError:
                        raise ValueError("Invalid PPM header: cannot parse max color")

                    if max_color != cls.MAX_COLOR_VALUE:
                        raise ValueError(f"Unsupported max color value: {max_color}")

                    header_complete = True

        # Parse pixel data
        expected_pixel_bytes = width * height * 3
        pixel_data = data[pos : pos + expected_pixel_bytes]

        if len(pixel_data) < expected_pixel_bytes:
            raise ValueError("Insufficient pixel data in PPM")

        pixels = []
        for y in range(height):
            row = []
            for x in range(width):
                pixel_idx = (y * width + x) * 3
                r, g, b = struct.unpack("BBB", pixel_data[pixel_idx : pixel_idx + 3])
                row.append((r, g, b))
            pixels.append(row)

        result = {
            "pixels": pixels,
            "width": width,
            "height": height,
            "x_offset": ft_data.get("x_offset", 0),
            "y_offset": ft_data.get("y_offset", 0),
            "layer": ft_data.get("layer", 0),
        }

        return result

    @classmethod
    def create_blank(cls, width: int, height: int, color: Optional[Color] = None) -> bytes:
        """Create a blank PPM frame filled with a single color.

        Args:
            width: Frame width
            height: Frame height
            color: Fill color (default: black)

        Returns:
            PPM binary data
        """
        if color is None:
            color = Color.BLACK

        # Create pixel grid
        pixels = [[(color.r, color.g, color.b) for _ in range(width)] for _ in range(height)]

        return cls.encode(pixels)

    @classmethod
    def resize_frame(
        cls, data: bytes, new_width: int, new_height: int, scale_mode: str = "nearest"
    ) -> bytes:
        """Resize a PPM frame to new dimensions.

        Args:
            data: Original PPM data
            new_width: New width
            new_height: New height
            scale_mode: "nearest" for nearest-neighbor scaling

        Returns:
            Resized PPM binary data
        """
        decoded = cls.decode(data)
        old_pixels = decoded["pixels"]
        old_height = len(old_pixels)
        old_width = len(old_pixels[0]) if old_pixels else 0

        if scale_mode != "nearest":
            raise ValueError(f"Unsupported scale mode: {scale_mode}")

        # Nearest-neighbor scaling
        new_pixels = []
        for y in range(new_height):
            row = []
            src_y = int((y / new_height) * old_height)
            src_y = min(src_y, old_height - 1)

            for x in range(new_width):
                src_x = int((x / new_width) * old_width)
                src_x = min(src_x, old_width - 1)

                row.append(old_pixels[src_y][src_x])

            new_pixels.append(row)

        return cls.encode(
            new_pixels,
            x_offset=decoded.get("x_offset", 0),
            y_offset=decoded.get("y_offset", 0),
            layer=decoded.get("layer", 0),
        )
