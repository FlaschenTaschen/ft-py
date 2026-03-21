"""
Hack - Rotating 3D text display with blur effect
Ported from hack.cc

Renders text with a vector font that rotates in 3D space with perspective projection.
Each character cycles through a 45-frame rotation animation.
Palette and border effects create a dynamic visual display.
"""

import math
from flaschen_taschen.demos import Demo
from flaschen_taschen.client.color import Color
from flaschen_taschen.standard_options import StandardOptions


# Vector font: 36 characters (0-9, A-Z), detailed outlines
# Each line is [x1, y1, x2, y2]
HACK_FONT = [
    # 0
    [[-2,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-2, 6],[-2, 6,-4, 4],[-4, 4,-4,-4],[-4,-4,-2,-6],[-2,-4, 2,-4],[ 2,-4, 2, 4],[ 2, 4,-2, 4],[-2, 4,-2,-4]],
    # 1
    [[ 1,-2,-1, 0],[-1, 0,-3, 0],[-3, 0, 1,-6],[ 1,-6, 3,-6],[ 3,-6, 3, 6],[ 3, 6, 1, 6],[ 1, 6, 1,-2]],
    # 2
    [[-4,-2,-4,-4],[-4,-4,-2,-6],[-2,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4,-2],[ 4,-2,-2, 4],[-2, 4, 4, 4],[ 4, 4, 4, 6],[ 4, 6,-4, 6],[-4, 6,-4, 4],[-4, 4, 2,-2],[ 2,-2, 2,-4],[ 2,-4,-2,-4],[-2,-4,-2,-2],[-2,-2,-4,-2]],
    # 3
    [[-4,-2,-4,-4],[-4,-4,-2,-6],[-2,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4,-2],[ 4,-2, 2, 0],[ 2, 0, 4, 2],[ 4, 2, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-2, 6],[-2, 6,-4, 4],[-4, 4,-4, 2],[-4, 2,-2, 2],[-2, 2,-2, 4],[-2, 4, 2, 4],[ 2, 4, 2, 2],[ 2, 2, 0, 0],[ 0, 0, 2,-2],[ 2,-2, 2,-4],[ 2,-4,-2,-4],[-2,-4,-2,-2],[-2,-2,-4,-2]],
    # 4
    [[-4,-6,-2,-6],[-2,-6,-2,-2],[-2,-2, 2,-2],[ 2,-2, 2,-6],[ 2,-6, 4,-6],[ 4,-6, 4, 6],[ 4, 6, 2, 6],[ 2, 6, 2, 0],[ 2, 0,-4, 0],[-4, 0,-4,-6]],
    # 5
    [[ 4,-6,-4,-6],[-4,-6,-4, 0],[-4, 0, 0, 0],[ 0, 0, 2, 2],[ 2, 2, 0, 4],[ 0, 4,-4, 4],[-4, 4,-4, 6],[-4, 6, 2, 6],[ 2, 6, 4, 4],[ 4, 4, 4, 0],[ 4, 0, 2,-2],[ 2,-2,-2,-2],[-2,-2,-2,-4],[-2,-4, 4,-4],[ 4,-4, 4,-6]],
    # 6
    [[ 4,-6, 4,-4],[ 4,-4,-2,-4],[-2,-4,-2,-2],[-2,-2, 2,-2],[ 2,-2, 4, 0],[ 4, 0, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-2, 6],[-2, 6,-4, 4],[-4, 4,-4,-4],[-4,-4,-2,-6],[-2,-6, 4,-6],[-2, 0, 2, 0],[ 2, 0, 2, 4],[ 2, 4,-2, 4],[-2, 4,-2, 0]],
    # 7
    [[-4,-6, 4,-6],[ 4,-6, 4,-4],[ 4,-4, 0, 6],[ 0, 6,-2, 6],[-2, 6, 2,-4],[ 2,-4,-4,-4],[-4,-4,-4,-6]],
    # 8
    [[-2,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4,-2],[ 4,-2, 2, 0],[ 2, 0, 4, 2],[ 4, 2, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-2, 6],[-2, 6,-4, 4],[-4, 4,-4, 2],[-4, 2,-2, 0],[-2, 0,-4,-2],[-4,-2,-4,-4],[-4,-4,-2,-6],[-2,-4, 2,-4],[ 2,-4, 2,-2],[ 2,-2,-2,-2],[-2,-2,-2,-4],[-2, 4, 2, 4],[ 2, 4, 2, 2],[ 2, 2,-2, 2],[-2, 2,-2, 4]],
    # 9
    [[-2,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-2, 6],[-2, 6,-4, 4],[-4, 4,-4, 2],[-4, 2,-2, 2],[-2, 2,-2, 4],[-2, 4, 2, 4],[ 2, 4, 2, 0],[ 2, 0,-2, 0],[-2, 0,-4,-2],[-4,-2,-4,-4],[-4,-4,-2,-6],[-2,-4, 2,-4],[ 2,-4, 2,-2],[ 2,-2,-2,-2],[-2,-2,-2,-4]],
    # A
    [[-2,-6, 2,-6],[ 2,-6, 4,-2],[ 4,-2, 4, 6],[ 4, 6, 2, 6],[ 2, 6, 2, 2],[ 2, 2,-2, 2],[-2, 2,-2, 6],[-2, 6,-4, 6],[-4, 6,-4,-2],[-4,-2,-2,-6],[ 0,-4, 2, 0],[ 2, 0,-2, 0],[-2, 0, 0,-4]],
    # B
    [[-4,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4,-2],[ 4,-2, 2, 0],[ 2, 0, 4, 2],[ 4, 2, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-4, 6],[-4, 6,-4,-6],[-2,-4, 2,-4],[ 2,-4, 2,-2],[ 2,-2,-2,-2],[-2,-2,-2,-4],[-2, 2, 2, 2],[ 2, 2, 2, 4],[ 2, 4,-2, 4],[-2, 4,-2, 2]],
    # C
    [[ 4,-6,-2,-6],[-2,-6,-4,-4],[-4,-4,-4, 4],[-4, 4,-2, 6],[-2, 6, 4, 6],[ 4, 6, 4, 4],[ 4, 4, 0, 4],[ 0, 4,-2, 2],[-2, 2,-2,-2],[-2,-2, 0,-4],[ 0,-4, 4,-4],[ 4,-4, 4,-6]],
    # D
    [[-4,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-4, 6],[-4, 6,-4,-6],[-2,-4, 2,-4],[ 2,-4, 2, 4],[ 2, 4,-2, 4],[-2, 4,-2,-4]],
    # E
    [[ 4,-6,-4,-6],[-4,-6,-4, 6],[-4, 6, 4, 6],[ 4, 6, 4, 4],[ 4, 4,-2, 4],[-2, 4,-2, 0],[-2, 0, 2, 0],[ 2, 0, 2,-2],[ 2,-2,-2,-2],[-2,-2,-2,-4],[-2,-4, 4,-4],[ 4,-4, 4,-6]],
    # F
    [[ 4,-6,-4,-6],[-4,-6,-4, 6],[-4, 6,-2, 6],[-2, 6,-2, 0],[-2, 0, 2, 0],[ 2, 0, 2,-2],[ 2,-2,-2,-2],[-2,-2,-2,-4],[-2,-4, 4,-4],[ 4,-4, 4,-6]],
    # G
    [[ 0, 0, 4, 0],[ 4, 0, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-2, 6],[-2, 6,-4, 4],[-4, 4,-4,-4],[-4,-4,-2,-6],[-2,-6, 4,-6],[ 4,-6, 4,-4],[ 4,-4, 0,-4],[ 0,-4,-2,-2],[-2,-2,-2, 2],[-2, 2, 0, 4],[ 0, 4, 2, 4],[ 2, 4, 2, 2],[ 2, 2, 0, 2],[ 0, 2, 0, 0]],
    # H
    [[-4,-6,-2,-6],[-2,-6,-2,-2],[-2,-2, 2,-2],[ 2,-2, 2,-6],[ 2,-6, 4,-6],[ 4,-6, 4, 6],[ 4, 6, 2, 6],[ 2, 6, 2, 0],[ 2, 0,-2, 0],[-2, 0,-2, 6],[-2, 6,-4, 6],[-4, 6,-4,-6]],
    # I
    [[-1,-6, 1,-6],[ 1,-6, 1, 6],[ 1, 6,-1, 6],[-1, 6,-1,-6]],
    # J
    [[ 1,-6, 3,-6],[ 3,-6, 3, 4],[ 3, 4, 1, 6],[ 1, 6,-1, 6],[-1, 6,-3, 4],[-3, 4,-3, 2],[-3, 2,-1, 2],[-1, 2,-1, 4],[-1, 4, 1, 4],[ 1, 4, 1,-6]],
    # K
    [[-4,-6,-2,-6],[-2,-6,-2,-2],[-2,-2, 2,-6],[ 2,-6, 4,-6],[ 4,-6, 0, 0],[ 0, 0, 4, 6],[ 4, 6, 2, 6],[ 2, 6,-2, 2],[-2, 2,-2, 6],[-2, 6,-4, 6],[-4, 6,-4,-6]],
    # L
    [[-3,-6,-1,-6],[-1,-6,-1, 4],[-1, 4, 3, 4],[ 3, 4, 3, 6],[ 3, 6,-3, 6],[-3, 6,-3,-6]],
    # M
    [[-4,-6, 0,-2],[ 0,-2, 4,-6],[ 4,-6, 4, 6],[ 4, 6, 2, 6],[ 2, 6, 2,-2],[ 2,-2, 0, 0],[ 0, 0,-2,-2],[-2,-2,-2, 6],[-2, 6,-4, 6],[-4, 6,-4,-6]],
    # N
    [[-3,-6,-1,-6],[-1,-6, 1, 0],[ 1, 0, 1,-6],[ 1,-6, 3,-6],[ 3,-6, 3, 6],[ 3, 6, 1, 6],[ 1, 6,-1, 0],[-1, 0,-1, 6],[-1, 6,-3, 6],[-3, 6,-3,-6]],
    # O
    [[-2,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-2, 6],[-2, 6,-4, 4],[-4, 4,-4,-4],[-4,-4,-2,-6],[-2,-4, 2,-4],[ 2,-4, 2, 4],[ 2, 4,-2, 4],[-2, 4,-2,-4]],
    # P
    [[-4,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4, 0],[ 4, 0, 2, 2],[ 2, 2,-2, 2],[-2, 2,-2, 6],[-2, 6,-4, 6],[-4, 6,-4,-6],[-2,-4, 2,-4],[ 2,-4, 2, 0],[ 2, 0,-2, 0],[-2, 0,-2,-4]],
    # Q
    [[-1,-6, 1,-6],[ 1,-6, 3,-4],[ 3,-4, 3, 4],[ 3, 4, 5, 6],[ 5, 6,-1, 6],[-1, 6,-3, 4],[-3, 4,-3,-4],[-3,-4,-1,-6],[-1,-4, 1,-4],[ 1,-4, 1, 4],[ 1, 4,-1, 4],[-1, 4,-1,-4]],
    # R
    [[-4,-6, 2,-6],[ 2,-6, 4,-4],[ 4,-4, 4, 0],[ 4, 0, 2, 2],[ 2, 2, 4, 6],[ 4, 6, 2, 6],[ 2, 6, 0, 2],[ 0, 2,-2, 2],[-2, 2,-2, 6],[-2, 6,-4, 6],[-4, 6,-4,-6],[-2,-4, 2,-4],[ 2,-4, 2, 0],[ 2, 0,-2, 0],[-2, 0,-2,-4]],
    # S
    [[ 4,-6,-2,-6],[-2,-6,-4,-4],[-4,-4,-4,-2],[-4,-2,-2, 0],[-2, 0, 2, 0],[ 2, 0, 2, 4],[ 2, 4,-4, 4],[-4, 4,-4, 6],[-4, 6, 2, 6],[ 2, 6, 4, 4],[ 4, 4, 4, 0],[ 4, 0, 2,-2],[ 2,-2,-2,-2],[-2,-2,-2,-4],[-2,-4, 4,-4],[ 4,-4, 4,-6]],
    # T
    [[-3,-6, 3,-6],[ 3,-6, 3,-4],[ 3,-4, 1,-4],[ 1,-4, 1, 6],[ 1, 6,-1, 6],[-1, 6,-1,-4],[-1,-4,-3,-4],[-3,-4,-3,-6]],
    # U
    [[-4,-6,-2,-6],[-2,-6,-2, 4],[-2, 4, 2, 4],[ 2, 4, 2,-6],[ 2,-6, 4,-6],[ 4,-6, 4, 4],[ 4, 4, 2, 6],[ 2, 6,-2, 6],[-2, 6,-4, 4],[-4, 4,-4,-6]],
    # V
    [[-4,-6,-2,-6],[-2,-6, 0, 4],[ 0, 4, 2,-6],[ 2,-6, 4,-6],[ 4,-6, 2, 6],[ 2, 6,-2, 6],[-2, 6,-4,-6]],
    # W
    [[-6,-6,-4,-6],[-4,-6,-2, 4],[-2, 4, 0,-2],[ 0,-2, 2, 4],[ 2, 4, 4,-6],[ 4,-6, 6,-6],[ 6,-6, 4, 6],[ 4, 6, 2, 6],[ 2, 6, 0, 4],[ 0, 4,-2, 6],[-2, 6,-4, 6],[-4, 6,-6,-6]],
    # X
    [[-4,-6,-2,-6],[-2,-6, 0,-2],[ 0,-2, 2,-6],[ 2,-6, 4,-6],[ 4,-6, 2, 0],[ 2, 0, 4, 6],[ 4, 6, 2, 6],[ 2, 6, 0, 2],[ 0, 2,-2, 6],[-2, 6,-4, 6],[-4, 6,-2, 0],[-2, 0,-4,-6]],
    # Y
    [[-4,-6,-2,-6],[-2,-6, 0,-2],[ 0,-2, 2,-6],[ 2,-6, 4,-6],[ 4,-6, 1, 0],[ 1, 0, 1, 6],[ 1, 6,-1, 6],[-1, 6,-1, 0],[-1, 0,-4,-6]],
    # Z
    [[-3,-6, 3,-6],[ 3,-6, 3,-4],[ 3,-4,-1, 4],[-1, 4, 3, 4],[ 3, 4, 3, 6],[ 3, 6,-3, 6],[-3, 6,-3, 4],[-3, 4, 1,-4],[ 1,-4,-3,-4],[-3,-4,-3,-6]]
]


class Hack(Demo):
    """
    Rotating 3D text animation with vector font.

    The demo:
    - Renders characters with a vector font that rotates in 3D
    - Each character displays for 45 frames with 8-degree rotation increments
    - Uses perspective projection for 3D effect
    - Applies blur and border effects
    - Cycles through 3 color palettes every 200 frames
    """

    def __init__(self, std_opts):
        super().__init__(std_opts)
        self.text = "HACK"
        self.palette_num = 1  # 1=Nebula, 2=Fire, 3=Bluegreen
        self.frame_count = 0

        # Parse demo-specific arguments
        args = std_opts.non_standard_args
        i = 0
        while i < len(args) and args[i].startswith('-'):
            arg = args[i]
            option = arg[1:]

            if option == 'p':
                i += 1
                if i < len(args):
                    try:
                        palette = int(args[i])
                        if 1 <= palette <= 3:
                            self.palette_num = palette
                    except ValueError:
                        pass

            i += 1

        # Collect remaining non-option arguments as text
        if i < len(args):
            self.text = ' '.join(args[i:]).upper()

    def setup(self):
        """Initialize pixel buffer and palette."""
        super().setup()
        self.pixels = [0] * (self.canvas.width * self.canvas.height)
        self.palette = self._create_palette(self.palette_num)
        self.char_codes = self._text_to_char_codes(self.text)

    def update(self):
        """Advance frame counter."""
        self.frame_count += 1

    def draw(self):
        """Draw rotating 3D text with effects."""
        # Update palette every 200 frames
        if self.frame_count % 200 == 0:
            self.palette_num = (self.palette_num % 3) + 1
            self.palette = self._create_palette(self.palette_num)

        # Draw border
        self._draw_box(0, 0, self.canvas.width - 1, self.canvas.height - 1, 0)

        # Apply blur and decay effect to previous frame's residual pixels
        self._blur()

        # Draw rotating character
        if self.char_codes:
            char_index = (self.frame_count // 45) % len(self.char_codes)
            frame_in_char = self.frame_count % 45
            angle = frame_in_char * 8  # 8 degrees per frame
            self._draw_hack_char(self.char_codes[char_index], angle, 0xFF)

        # Copy pixels to canvas
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                idx = y * self.canvas.width + x
                self.canvas.set_pixel(x, y, self.palette[self.pixels[idx]])

    def _text_to_char_codes(self, text):
        """Convert text to character codes for the vector font."""
        char_codes = []
        for char in text:
            if '0' <= char <= '9':
                char_codes.append(ord(char) - ord('0'))
            elif 'A' <= char <= 'Z':
                char_codes.append(ord(char) - ord('A') + 10)
        return char_codes

    def _draw_hack_char(self, charcode, angle, color):
        """Draw a rotating 3D character."""
        if charcode < 0 or charcode >= len(HACK_FONT):
            return

        hw = self.canvas.width >> 1
        hh = self.canvas.height >> 1
        D = 32
        Z = 15

        # Convert angle to radians
        angle_rad = math.radians(angle)
        cs = math.cos(angle_rad)
        sn = math.sin(angle_rad)

        for line_segment in HACK_FONT[charcode]:
            if len(line_segment) < 4:
                continue

            x1, y1, x2, y2 = line_segment

            # 3D rotation around Y axis with perspective projection
            sx1 = x1 * cs
            sy1 = y1
            sz1 = x1 * sn + Z

            sx2 = x2 * cs
            sy2 = y2
            sz2 = x2 * sn + Z

            # Avoid division by zero
            sz1_safe = sz1 if sz1 != 0 else 1.0
            sz2_safe = sz2 if sz2 != 0 else 1.0

            # Perspective projection
            px1 = int(D * sx1 / sz1_safe)
            py1 = int(D * sy1 / sz1_safe)
            px2 = int(D * sx2 / sz2_safe)
            py2 = int(D * sy2 / sz2_safe)

            # Draw line with offset to center
            self._draw_line(px1 + hw, py1 + hh, px2 + hw, py2 + hh, color)

    def _draw_line(self, x1, y1, x2, y2, color):
        """Draw a thick line using Bresenham's algorithm."""
        x = x1
        y = y1
        deltax = abs(x2 - x1)
        deltay = abs(y2 - y1)
        xinc = 1 if x2 >= x1 else -1
        yinc = 1 if y2 >= y1 else -1

        if deltax >= deltay:
            num_add = deltay
            num_pixels = deltax
            num = deltax // 2

            for _ in range(num_pixels + 1):
                self._set_pixel(x, y, color)
                self._set_pixel(x, y + 1, color)
                num += num_add
                if num >= deltax:
                    num -= deltax
                    y += yinc
                x += xinc
        else:
            num_add = deltax
            num_pixels = deltay
            num = deltay // 2

            for _ in range(num_pixels + 1):
                self._set_pixel(x, y, color)
                self._set_pixel(x + 1, y, color)
                num += num_add
                if num >= deltay:
                    num -= deltay
                    x += xinc
                y += yinc

    def _set_pixel(self, x, y, color):
        """Set pixel in buffer with bounds checking."""
        if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
            self.pixels[y * self.canvas.width + x] = color

    def _draw_box(self, x1, y1, x2, y2, color):
        """Draw rectangle outline."""
        for x in range(x1, x2 + 1):
            if 0 <= y1 < self.canvas.height:
                self.pixels[y1 * self.canvas.width + x] = color
            if 0 <= y2 < self.canvas.height:
                self.pixels[y2 * self.canvas.width + x] = color
        for y in range(y1, y2 + 1):
            if 0 <= x1 < self.canvas.width:
                self.pixels[y * self.canvas.width + x1] = color
            if 0 <= x2 < self.canvas.width:
                self.pixels[y * self.canvas.width + x2] = color

    def _blur(self):
        """Apply blur and decay effect."""
        blur_drop = 32
        size = self.canvas.width * (self.canvas.height - 1) - 1

        for i in range(size):
            avg = ((self.pixels[i] + self.pixels[i + 1] +
                    self.pixels[i + self.canvas.width] +
                    self.pixels[i + self.canvas.width + 1]) >> 2) & 0xFF
            dot = 0 if avg <= blur_drop else (avg - blur_drop)
            self.pixels[i] = dot

    def _create_palette(self, palette_num):
        """Generate color palette."""
        palette = [Color(0, 0, 0)] * 256

        if palette_num == 1:
            # Nebula: black -> blue -> blue-violet -> red -> white
            self._add_gradient(palette, 0, 63, 0, 0, 0, 0, 0, 127)
            self._add_gradient(palette, 64, 127, 0, 0, 127, 127, 0, 255)
            self._add_gradient(palette, 128, 191, 127, 0, 255, 255, 0, 0)
            self._add_gradient(palette, 192, 255, 255, 0, 0, 255, 255, 255)

        elif palette_num == 2:
            # Fire: black -> blue -> red -> yellow -> white
            self._add_gradient(palette, 0, 63, 0, 0, 0, 0, 0, 127)
            self._add_gradient(palette, 64, 127, 0, 0, 127, 255, 0, 0)
            self._add_gradient(palette, 128, 191, 255, 0, 0, 255, 255, 0)
            self._add_gradient(palette, 192, 255, 255, 255, 0, 255, 255, 255)

        elif palette_num == 3:
            # Bluegreen: black -> blue -> teal -> green -> white
            self._add_gradient(palette, 0, 63, 0, 0, 0, 0, 0, 127)
            self._add_gradient(palette, 64, 127, 0, 0, 127, 0, 127, 255)
            self._add_gradient(palette, 128, 191, 0, 127, 255, 0, 255, 0)
            self._add_gradient(palette, 192, 255, 0, 255, 0, 255, 255, 255)

        return palette

    @staticmethod
    def _add_gradient(palette, start, end, r1, g1, b1, r2, g2, b2):
        """Add a color gradient to the palette."""
        range_val = end - start
        for i in range(range_val + 1):
            k = i / range_val if range_val > 0 else 0
            r = int(r1 + (r2 - r1) * k)
            g = int(g1 + (g2 - g1) * k)
            b = int(b1 + (b2 - b1) * k)
            palette[start + i] = Color(r, g, b)


if __name__ == '__main__':
    from flaschen_taschen.demos import run_demo
    run_demo(Hack)
