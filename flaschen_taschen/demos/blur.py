"""Blur demo: Draw random shapes and apply repeated blur filtering.

Demonstrates simple 2x2 blur with decay applied to create fading/blurred effect.
Supports multiple shape types: bolt, boxes, circles, target, fire.
Supports 3 color palettes: 1=Nebula, 2=Fire, 3=Bluegreen (default: cycles).
Matches C++ blur implementation exactly.
"""

import random
from flaschen_taschen.client.color import Color, create_hsv_palette
from flaschen_taschen.demos import Demo, run_demo


class BlurDemo(Demo):
    """Draw random shapes and apply blur filtering with decay."""

    def setup(self) -> None:
        """Initialize blur parameters."""
        super().setup()
        assert self.canvas is not None

        # Parse demo type from non-standard args
        self.demo_type = "bolt"  # Default
        self.palette_num = -1  # -1 = cycle

        if self.std_opts.non_standard_args:
            for arg in self.std_opts.non_standard_args:
                arg_lower = arg.lower()
                if arg_lower in ["all", "bolt", "boxes", "circles", "target", "fire"]:
                    self.demo_type = arg_lower
                elif arg_lower.startswith("-p"):
                    # Handle -p as a prefix (e.g., "-p1" or "-p 1")
                    try:
                        if arg_lower == "-p" and len(self.std_opts.non_standard_args) > 1:
                            # -p is separate, next arg should be palette num
                            idx = self.std_opts.non_standard_args.index(arg)
                            if idx + 1 < len(self.std_opts.non_standard_args):
                                self.palette_num = int(self.std_opts.non_standard_args[idx + 1])
                        else:
                            # Try to parse -p1, -p2, etc.
                            num_str = arg_lower[2:] if len(arg_lower) > 2 else ""
                            if num_str:
                                self.palette_num = int(num_str)
                    except (ValueError, IndexError):
                        pass

        # Initialize 1D pixel buffer (linear array like Swift)
        self.pixels = [0] * (self.canvas.width * self.canvas.height)
        self.w = self.canvas.width
        self.h = self.canvas.height

        # Initialize palette (default to palette 1 = Nebula)
        self.current_palette_num = 1 if self.palette_num < 0 else self.palette_num
        self.palette = self._create_palette(self.current_palette_num)

        # Demo sequence for "all" mode
        self.frame_count = 0
        self.current_demo = "bolt" if self.demo_type == "all" else self.demo_type

    def update(self) -> None:
        """Update animation state."""
        self.frame_count += 1

        # Cycle palettes every 100 frames if palette_num < 0 (cycling mode)
        if self.palette_num < 0 and self.frame_count % 100 == 0:
            self.current_palette_num += 1
            if self.current_palette_num > 8:  # Cycle through all 9 palettes (0-8)
                self.current_palette_num = 0
            self.palette = self._create_palette(self.current_palette_num)

        # Cycle through demos if "all" mode
        if self.demo_type == "all" and self.frame_count % 300 == 0:
            demos = ["bolt", "boxes", "circles", "target", "fire"]
            idx = demos.index(self.current_demo)
            self.current_demo = demos[(idx + 1) % len(demos)]

    def draw(self) -> None:
        """Draw shape and apply blur."""
        assert self.canvas is not None

        # Draw shape on even frames only
        if self.frame_count % 2 == 0:
            if self.current_demo == "bolt":
                self._draw_random_bolt()
            elif self.current_demo == "boxes":
                self._draw_random_box()
            elif self.current_demo == "circles":
                self._draw_random_circle()
            elif self.current_demo == "target":
                self._draw_random_target()
            elif self.current_demo == "fire":
                self._draw_random_fire()

        # Apply blur filter
        if self.current_demo == "fire":
            self._blur_fire()
        else:
            self._blur3()

        # Convert pixel buffer to canvas colors
        for y in range(self.h):
            for x in range(self.w):
                intensity = self.pixels[y * self.w + x]
                palette_idx = min(255, max(0, intensity))
                color = self.palette[palette_idx]
                self.canvas.set_pixel(x, y, color)

    def _draw_box(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Draw box outline at specified coordinates."""
        # Top and bottom edges
        for x in range(x1, x2 + 1):
            if y1 < self.h:
                self.pixels[y1 * self.w + x] = 0xFF
            if y2 < self.h:
                self.pixels[y2 * self.w + x] = 0xFF
        # Left and right edges
        for y in range(y1, y2 + 1):
            self.pixels[y * self.w + x1] = 0xFF
            self.pixels[y * self.w + x2] = 0xFF

    def _draw_random_box(self) -> None:
        """Draw random box outline."""
        x1 = random.randint(0, self.w - 2)
        y1 = random.randint(0, self.h - 2)
        x2 = random.randint(x1, self.w - 1)
        y2 = random.randint(y1, self.h - 1)
        self._draw_box(x1, y1, x2, y2)

    def _set_pixel(self, x: int, y: int, color: int) -> None:
        """Set pixel in 1D buffer with bounds checking."""
        if 0 <= x < self.w and 0 <= y < self.h:
            self.pixels[y * self.w + x] = color

    def _draw_circle(self, x0: int, y0: int, radius: int, color: int) -> None:
        """Draw circle using Midpoint circle algorithm."""
        x = radius
        y = 0
        radius_error = 1 - x

        while y <= x:
            self._set_pixel(x0 + x, y0 + y, color)
            self._set_pixel(x0 + y, y0 + x, color)
            self._set_pixel(x0 - x, y0 + y, color)
            self._set_pixel(x0 - y, y0 + x, color)
            self._set_pixel(x0 - x, y0 - y, color)
            self._set_pixel(x0 - y, y0 - x, color)
            self._set_pixel(x0 + x, y0 - y, color)
            self._set_pixel(x0 + y, y0 - x, color)

            y += 1
            if radius_error < 0:
                radius_error += 2 * y + 1
            else:
                x -= 1
                radius_error += 2 * (y - x + 1)

    def _draw_random_circle(self) -> None:
        """Draw random circle outline."""
        x0 = random.randint(0, self.w - 2)
        y0 = random.randint(0, self.h - 2)
        radius = random.randint(2, self.w // 3)
        self._draw_circle(x0, y0, radius, 0xFF)

    def _draw_random_target(self) -> None:
        """Draw target: single circle centered at display center."""
        x0 = self.w // 2
        y0 = self.w // 2  # Note: uses width for y0 like Swift
        radius = random.randint(2, self.w // 2)
        self._draw_circle(x0, y0, radius, 0xFF)

    def _draw_random_bolt(self) -> None:
        """Draw random lightning bolt (wavy horizontal line)."""
        hh = self.h >> 1  # height / 2
        wave = 0

        for x in range(self.w):
            wave += random.randint(-1, 1)
            y = hh + wave
            if y < 0 or y >= self.h:
                y = hh
            self.pixels[y * self.w + x] = 0xFF

    def _draw_random_fire(self) -> None:
        """Draw random fire: pixels at bottom edge (orient=0)."""
        num = random.randint(1, self.w - 2)
        for _ in range(num):
            x = random.randint(1, self.w - 2)
            y = self.h - 1
            self.pixels[y * self.w + x] = 0xFF

    def _blur3(self) -> None:
        """Apply 2x2 blur with decay (matches Swift blur3)."""
        i = 0

        # Process all but last row
        for _ in range(self.h - 1):
            for _ in range(self.w - 1):
                dot1 = self.pixels[i]
                dot2 = self.pixels[i + 1]
                dot3 = self.pixels[i + self.w]
                dot4 = self.pixels[i + self.w + 1]
                dot = (dot1 + dot2 + dot3 + dot4) >> 2
                dot = 0 if dot <= 8 else dot - 8
                self.pixels[i] = dot
                i += 1

            # Handle last pixel in row
            dot1 = self.pixels[i]
            dot2 = self.pixels[i + self.w]
            dot = (dot1 + dot2) >> 2
            dot = 0 if dot <= 8 else dot - 8
            self.pixels[i] = dot
            i += 1

        # Process last row
        for _ in range(self.w - 1):
            dot1 = self.pixels[i]
            dot2 = self.pixels[i + 1]
            dot = (dot1 + dot2) >> 2
            dot = 0 if dot <= 8 else dot - 8
            self.pixels[i] = dot
            i += 1

        # Last pixel
        self.pixels[i] = 0

    @staticmethod
    def _color_gradient(start: int, end: int, r1: int, g1: int, b1: int, r2: int, g2: int, b2: int) -> list:
        """Generate color gradient from (r1,g1,b1) to (r2,g2,b2)."""
        gradient = []
        num_colors = end - start + 1
        for i in range(num_colors):
            k = i / (num_colors - 1) if num_colors > 1 else 0
            r = int(r1 + (r2 - r1) * k)
            g = int(g1 + (g2 - g1) * k)
            b = int(b1 + (b2 - b1) * k)
            gradient.append(Color(r, g, b))
        return gradient

    @staticmethod
    def _create_palette(palette_num: int) -> list:
        """Create color palette for blur effect.

        Args:
            palette_num: 0=Rainbow, 1=Nebula, 2=Fire, 3=Bluegreen, 4=Colorful,
                        5=Magma, 6=Inferno, 7=Plasma, 8=Viridis

        Returns:
            List of 256 Color objects
        """
        palette = [Color.BLACK] * 256

        if palette_num == 0:
            # Rainbow: red -> yellow -> green -> cyan -> blue -> magenta
            palette[0:43] = BlurDemo._color_gradient(0, 42, 255, 0, 0, 255, 255, 0)
            palette[43:86] = BlurDemo._color_gradient(43, 85, 255, 255, 0, 0, 255, 0)
            palette[86:129] = BlurDemo._color_gradient(86, 128, 0, 255, 0, 0, 255, 255)
            palette[129:171] = BlurDemo._color_gradient(129, 170, 0, 255, 255, 0, 0, 255)
            palette[171:214] = BlurDemo._color_gradient(171, 213, 0, 0, 255, 255, 0, 255)
            palette[214:256] = BlurDemo._color_gradient(214, 255, 255, 0, 255, 255, 0, 0)

        elif palette_num == 1:
            # Nebula: black -> half blue -> blue-violet -> red -> white
            palette[0:32] = BlurDemo._color_gradient(0, 31, 1, 1, 1, 0, 0, 127)
            palette[32:96] = BlurDemo._color_gradient(32, 95, 0, 0, 127, 127, 0, 255)
            palette[96:160] = BlurDemo._color_gradient(96, 159, 127, 0, 255, 255, 0, 0)
            palette[160:192] = BlurDemo._color_gradient(160, 191, 255, 0, 0, 255, 255, 255)
            palette[192:256] = [Color.WHITE] * 64

        elif palette_num == 2:
            # Fire: black -> half blue -> red -> yellow -> white
            palette[0:32] = BlurDemo._color_gradient(0, 31, 1, 1, 1, 0, 0, 127)
            palette[32:96] = BlurDemo._color_gradient(32, 95, 0, 0, 127, 255, 0, 0)
            palette[96:160] = BlurDemo._color_gradient(96, 159, 255, 0, 0, 255, 255, 0)
            palette[160:192] = BlurDemo._color_gradient(160, 191, 255, 255, 0, 255, 255, 255)
            palette[192:256] = [Color.WHITE] * 64

        elif palette_num == 3:
            # Bluegreen: black -> half blue -> teal -> green -> white
            palette[0:32] = BlurDemo._color_gradient(0, 31, 1, 1, 1, 0, 0, 127)
            palette[32:96] = BlurDemo._color_gradient(32, 95, 0, 0, 127, 0, 127, 255)
            palette[96:160] = BlurDemo._color_gradient(96, 159, 0, 127, 255, 0, 255, 0)
            palette[160:192] = BlurDemo._color_gradient(160, 191, 0, 255, 0, 255, 255, 255)
            palette[192:256] = [Color.WHITE] * 64

        elif palette_num == 4:
            # Colorful: red-dominant -> magenta -> cyan -> white
            palette[0:64] = BlurDemo._color_gradient(0, 63, 0, 0, 0, 255, 0, 0)
            palette[64:128] = BlurDemo._color_gradient(64, 127, 255, 0, 0, 255, 0, 255)
            palette[128:192] = BlurDemo._color_gradient(128, 191, 255, 0, 255, 0, 255, 255)
            palette[192:256] = BlurDemo._color_gradient(192, 255, 0, 255, 255, 255, 255, 255)

        elif palette_num == 5:
            # Magma: black -> purple -> red -> yellow -> white
            palette[0:64] = BlurDemo._color_gradient(0, 63, 13, 11, 30, 75, 0, 130)
            palette[64:128] = BlurDemo._color_gradient(64, 127, 75, 0, 130, 255, 0, 0)
            palette[128:192] = BlurDemo._color_gradient(128, 191, 255, 0, 0, 255, 255, 0)
            palette[192:256] = BlurDemo._color_gradient(192, 255, 255, 255, 0, 255, 255, 255)

        elif palette_num == 6:
            # Inferno: black -> purple -> orange -> yellow -> white
            palette[0:64] = BlurDemo._color_gradient(0, 63, 0, 0, 4, 87, 16, 121)
            palette[64:128] = BlurDemo._color_gradient(64, 127, 87, 16, 121, 224, 92, 14)
            palette[128:192] = BlurDemo._color_gradient(128, 191, 224, 92, 14, 253, 231, 37)
            palette[192:256] = BlurDemo._color_gradient(192, 255, 253, 231, 37, 255, 255, 255)

        elif palette_num == 7:
            # Plasma: dark purple -> magenta -> cyan -> yellow -> white
            palette[0:64] = BlurDemo._color_gradient(0, 63, 13, 0, 51, 136, 0, 136)
            palette[64:128] = BlurDemo._color_gradient(64, 127, 136, 0, 136, 0, 255, 255)
            palette[128:192] = BlurDemo._color_gradient(128, 191, 0, 255, 255, 255, 255, 0)
            palette[192:256] = BlurDemo._color_gradient(192, 255, 255, 255, 0, 255, 255, 255)

        elif palette_num == 8:
            # Viridis: dark blue -> cyan -> green -> yellow
            palette[0:64] = BlurDemo._color_gradient(0, 63, 68, 1, 84, 59, 82, 139)
            palette[64:128] = BlurDemo._color_gradient(64, 127, 59, 82, 139, 33, 145, 140)
            palette[128:192] = BlurDemo._color_gradient(128, 191, 33, 145, 140, 253, 231, 37)
            palette[192:256] = BlurDemo._color_gradient(192, 255, 253, 231, 37, 255, 255, 255)

        return palette

    def _blur_fire(self) -> None:
        """Apply fire blur: 8-neighbor averaging with decay."""
        step = 4

        # Process interior pixels (excluding edges to avoid bounds issues)
        for i in range(1, self.w * (self.h - 2) - 1):
            vals = [
                self.pixels[i - 1],
                self.pixels[i + 1],
                self.pixels[i + self.w - 1],
                self.pixels[i + self.w],
                self.pixels[i + self.w + 1],
                self.pixels[i + 2 * self.w - 1],
                self.pixels[i + 2 * self.w],
                self.pixels[i + 2 * self.w + 1],
            ]
            dot = sum(vals) >> 3
            dot = 0 if dot <= step else dot - step
            self.pixels[i] = dot


if __name__ == "__main__":
    run_demo(BlurDemo)
