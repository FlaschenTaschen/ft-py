"""BDF (Bitmap Distribution Format) font parser and renderer."""

import os
from typing import Dict, List, Tuple, Optional


class BDFFont:
    """Parse and render BDF font files."""

    def __init__(self, font_path: str):
        """
        Initialize BDF font from file.

        Args:
            font_path: Path to .bdf font file
        """
        self.font_path = font_path
        self.char_width = 0
        self.char_height = 0
        self.baseline = 0
        self.characters: Dict[int, Dict] = {}

        self._parse_font()

    def _parse_font(self):
        """Parse BDF font file."""
        if not os.path.exists(self.font_path):
            raise FileNotFoundError(f"Font file not found: {self.font_path}")

        with open(self.font_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        in_char = False
        char_code = None
        char_width = None
        char_height = None
        char_x_offset = None
        char_y_offset = None
        bitmap_lines = []
        bitmap_index = 0

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1

            if line.startswith('FONTBOUNDINGBOX'):
                parts = line.split()
                if len(parts) >= 5:
                    self.char_width = int(parts[1])
                    self.char_height = int(parts[2])
                    # parts[3] is x_offset, parts[4] is y_offset

            elif line.startswith('STARTCHAR'):
                in_char = True
                bitmap_lines = []
                bitmap_index = 0

            elif line.startswith('ENCODING'):
                parts = line.split()
                if len(parts) >= 2:
                    char_code = int(parts[1])

            elif line.startswith('DWIDTH'):
                parts = line.split()
                if len(parts) >= 3:
                    char_width = int(parts[1])
                    # char_height stays from bounding box

            elif line.startswith('BBX'):
                parts = line.split()
                if len(parts) >= 5:
                    char_width = int(parts[1])
                    char_height = int(parts[2])
                    char_x_offset = int(parts[3])
                    char_y_offset = int(parts[4])

            elif line.startswith('BITMAP'):
                # Read bitmap data
                while i < len(lines):
                    bitmap_line = lines[i].strip()
                    i += 1

                    if bitmap_line.startswith('ENDCHAR'):
                        in_char = False
                        break

                    if bitmap_line:
                        bitmap_lines.append(bitmap_line)

                # Parse bitmap data (hex strings)
                if char_code is not None and bitmap_lines:
                    self.characters[char_code] = {
                        'width': char_width or self.char_width,
                        'height': char_height or self.char_height,
                        'x_offset': char_x_offset or 0,
                        'y_offset': char_y_offset or 0,
                        'bitmap': self._parse_bitmap(bitmap_lines, char_width or self.char_width, char_height or self.char_height),
                    }

    def _parse_bitmap(self, hex_lines: List[str], width: int, height: int) -> List[List[int]]:
        """
        Parse hex bitmap data into 2D pixel array.

        Args:
            hex_lines: List of hex strings
            width: Character width in pixels
            height: Character height in pixels

        Returns:
            2D list of pixels (1=on, 0=off)
        """
        # Calculate bytes per line (round up to nearest byte)
        bytes_per_line = (width + 7) // 8

        bitmap = []
        for hex_line in hex_lines[:height]:
            pixels = []

            # Convert hex string to binary
            hex_str = hex_line.strip()
            for i in range(bytes_per_line):
                if i * 2 < len(hex_str):
                    byte_val = int(hex_str[i * 2:i * 2 + 2], 16)
                else:
                    byte_val = 0

                # Extract individual bits
                for bit in range(8):
                    if len(pixels) < width:
                        pixels.append((byte_val >> (7 - bit)) & 1)

            # Pad to width if needed
            while len(pixels) < width:
                pixels.append(0)

            bitmap.append(pixels[:width])

        # Pad to height if needed
        while len(bitmap) < height:
            bitmap.append([0] * width)

        return bitmap

    def render_char(self, char: str) -> Optional[List[List[int]]]:
        """
        Render a single character.

        Args:
            char: Character to render

        Returns:
            2D list of pixels, or None if character not in font
        """
        char_code = ord(char)
        if char_code not in self.characters:
            # Try space as fallback
            if ord(' ') in self.characters:
                char_code = ord(' ')
            else:
                return None

        char_data = self.characters[char_code]
        return char_data['bitmap']

    def get_char_width(self, char: str = 'A') -> int:
        """Get width of a character (or default width)."""
        char_code = ord(char)
        if char_code in self.characters:
            return self.characters[char_code]['width']
        return self.char_width

    def get_char_height(self) -> int:
        """Get height of characters."""
        return self.char_height

    def get_text_width(self, text: str) -> int:
        """Get total width of rendered text."""
        total = 0
        for char in text:
            total += self.get_char_width(char)
        return total

    def get_text_height(self) -> int:
        """Get height of text."""
        return self.char_height
