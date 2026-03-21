"""Plasma demo: Animated plasma effect with sliding lookup tables.

Ported from PlasmaDemo.swift - uses pre-computed lookup tables with
sliding windows to create animated plasma effect. Supports numpy for
optional performance optimization.
"""

import math
import random

from flaschen_taschen.client.color import Color, create_hsv_palette
from flaschen_taschen.demos import Demo, run_demo

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


class PlasmaDemo(Demo):
    """Animated plasma effect with pre-computed lookup tables."""

    def setup(self) -> None:
        """Initialize plasma lookup tables and parameters."""
        super().setup()
        assert self.canvas is not None

        # Parse palette selection from -p flag
        self.palette_num = -1  # -1 = default (HSV)
        if self.std_opts.non_standard_args:
            for arg in self.std_opts.non_standard_args:
                arg_lower = arg.lower()
                if arg_lower.startswith("-p"):
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

        # Parameters matching Swift version
        self.lookup_quant = 20
        slowness = 100.0 / max(self.std_opts.delay, 1)  # Avoid division by zero
        self.slowness = slowness

        # Plasma lookup table dimensions
        self.plasma_width = self.lookup_quant * self.canvas.width * 2
        self.plasma_height = self.lookup_quant * self.canvas.height * 2
        self.center_x = self.lookup_quant * self.canvas.width
        self.center_y = self.lookup_quant * self.canvas.height

        # Pre-compute lookup tables (matches Swift exactly)
        self.plasma1 = self._compute_plasma1()
        self.plasma2 = self._compute_plasma2()

        # Sliding window half-sizes
        self.hw = self.lookup_quant * self.canvas.width // 2
        self.hh = self.lookup_quant * self.canvas.height // 2

        # Color palette (use selected palette)
        self.palette = self._create_palette(self.palette_num)

        # Animation counter
        self.count = random.uniform(0, 100000)
        self.lowest_value = 100.0
        self.highest_value = -100.0

    def _compute_plasma1(self) -> list:
        """Pre-compute first plasma lookup table (distance-based)."""
        plasma1 = []
        for y in range(self.plasma_height):
            row = []
            for x in range(self.plasma_width):
                dx = float(self.center_x - x)
                dy = float(self.center_y - y)
                value = math.sin(math.sqrt(dx * dx + dy * dy) / (4.0 * self.lookup_quant))
                row.append(value)
            plasma1.append(row)
        return plasma1

    def _compute_plasma2(self) -> list:
        """Pre-compute second plasma lookup table (sinusoidal pattern)."""
        plasma2 = []
        for y in range(self.plasma_height):
            row = []
            for x in range(self.plasma_width):
                x_norm = 4.0 * x / self.lookup_quant
                y_norm = 4.0 * y / self.lookup_quant
                denom1 = 37.0 + 15.0 * math.cos(y / (18.5 * self.lookup_quant))
                denom2 = 31.0 + 11.0 * math.sin(x / (14.25 * self.lookup_quant))
                value = math.sin(x_norm / denom1) * math.cos(y_norm / denom2)
                row.append(value)
            plasma2.append(row)
        return plasma2

    def _clamp(self, value: int, min_val: int, max_val: int) -> int:
        """Clamp value to range [min_val, max_val]."""
        if value < min_val:
            return min_val
        if value > max_val:
            return max_val
        return value

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
        """Create color palette for plasma effect.

        Args:
            palette_num: -1=HSV (default), 0=Rainbow, 1=Nebula, 2=Fire, 3=Bluegreen,
                        4=Colorful, 5=Magma, 6=Inferno, 7=Plasma, 8=Viridis

        Returns:
            List of 256 Color objects
        """
        if palette_num < 0:
            # Default: HSV palette
            palette_obj = create_hsv_palette(256)
            return palette_obj.colors

        palette = [Color.BLACK] * 256

        if palette_num == 0:
            # Rainbow: red -> yellow -> green -> cyan -> blue -> magenta
            palette[0:43] = PlasmaDemo._color_gradient(0, 42, 255, 0, 0, 255, 255, 0)
            palette[43:86] = PlasmaDemo._color_gradient(43, 85, 255, 255, 0, 0, 255, 0)
            palette[86:129] = PlasmaDemo._color_gradient(86, 128, 0, 255, 0, 0, 255, 255)
            palette[129:171] = PlasmaDemo._color_gradient(129, 170, 0, 255, 255, 0, 0, 255)
            palette[171:214] = PlasmaDemo._color_gradient(171, 213, 0, 0, 255, 255, 0, 255)
            palette[214:256] = PlasmaDemo._color_gradient(214, 255, 255, 0, 255, 255, 0, 0)

        elif palette_num == 1:
            # Nebula: black -> half blue -> blue-violet -> red -> white
            palette[0:32] = PlasmaDemo._color_gradient(0, 31, 1, 1, 1, 0, 0, 127)
            palette[32:96] = PlasmaDemo._color_gradient(32, 95, 0, 0, 127, 127, 0, 255)
            palette[96:160] = PlasmaDemo._color_gradient(96, 159, 127, 0, 255, 255, 0, 0)
            palette[160:192] = PlasmaDemo._color_gradient(160, 191, 255, 0, 0, 255, 255, 255)
            palette[192:256] = [Color.WHITE] * 64

        elif palette_num == 2:
            # Fire: black -> half blue -> red -> yellow -> white
            palette[0:32] = PlasmaDemo._color_gradient(0, 31, 1, 1, 1, 0, 0, 127)
            palette[32:96] = PlasmaDemo._color_gradient(32, 95, 0, 0, 127, 255, 0, 0)
            palette[96:160] = PlasmaDemo._color_gradient(96, 159, 255, 0, 0, 255, 255, 0)
            palette[160:192] = PlasmaDemo._color_gradient(160, 191, 255, 255, 0, 255, 255, 255)
            palette[192:256] = [Color.WHITE] * 64

        elif palette_num == 3:
            # Bluegreen: black -> half blue -> teal -> green -> white
            palette[0:32] = PlasmaDemo._color_gradient(0, 31, 1, 1, 1, 0, 0, 127)
            palette[32:96] = PlasmaDemo._color_gradient(32, 95, 0, 0, 127, 0, 127, 255)
            palette[96:160] = PlasmaDemo._color_gradient(96, 159, 0, 127, 255, 0, 255, 0)
            palette[160:192] = PlasmaDemo._color_gradient(160, 191, 0, 255, 0, 255, 255, 255)
            palette[192:256] = [Color.WHITE] * 64

        elif palette_num == 4:
            # Colorful: red-dominant -> magenta -> cyan -> white
            palette[0:64] = PlasmaDemo._color_gradient(0, 63, 0, 0, 0, 255, 0, 0)
            palette[64:128] = PlasmaDemo._color_gradient(64, 127, 255, 0, 0, 255, 0, 255)
            palette[128:192] = PlasmaDemo._color_gradient(128, 191, 255, 0, 255, 0, 255, 255)
            palette[192:256] = PlasmaDemo._color_gradient(192, 255, 0, 255, 255, 255, 255, 255)

        elif palette_num == 5:
            # Magma: black -> purple -> red -> yellow -> white
            palette[0:64] = PlasmaDemo._color_gradient(0, 63, 13, 11, 30, 75, 0, 130)
            palette[64:128] = PlasmaDemo._color_gradient(64, 127, 75, 0, 130, 255, 0, 0)
            palette[128:192] = PlasmaDemo._color_gradient(128, 191, 255, 0, 0, 255, 255, 0)
            palette[192:256] = PlasmaDemo._color_gradient(192, 255, 255, 255, 0, 255, 255, 255)

        elif palette_num == 6:
            # Inferno: black -> purple -> orange -> yellow -> white
            palette[0:64] = PlasmaDemo._color_gradient(0, 63, 0, 0, 4, 87, 16, 121)
            palette[64:128] = PlasmaDemo._color_gradient(64, 127, 87, 16, 121, 224, 92, 14)
            palette[128:192] = PlasmaDemo._color_gradient(128, 191, 224, 92, 14, 253, 231, 37)
            palette[192:256] = PlasmaDemo._color_gradient(192, 255, 253, 231, 37, 255, 255, 255)

        elif palette_num == 7:
            # Plasma: dark purple -> magenta -> cyan -> yellow -> white
            palette[0:64] = PlasmaDemo._color_gradient(0, 63, 13, 0, 51, 136, 0, 136)
            palette[64:128] = PlasmaDemo._color_gradient(64, 127, 136, 0, 136, 0, 255, 255)
            palette[128:192] = PlasmaDemo._color_gradient(128, 191, 0, 255, 255, 255, 255, 0)
            palette[192:256] = PlasmaDemo._color_gradient(192, 255, 255, 255, 0, 255, 255, 255)

        elif palette_num == 8:
            # Viridis: dark blue -> cyan -> green -> yellow
            palette[0:64] = PlasmaDemo._color_gradient(0, 63, 68, 1, 84, 59, 82, 139)
            palette[64:128] = PlasmaDemo._color_gradient(64, 127, 59, 82, 139, 33, 145, 140)
            palette[128:192] = PlasmaDemo._color_gradient(128, 191, 33, 145, 140, 253, 231, 37)
            palette[192:256] = PlasmaDemo._color_gradient(192, 255, 253, 231, 37, 255, 255, 255)

        return palette

    def update(self) -> None:
        """Update animation counter."""
        self.count += 1

    def draw(self) -> None:
        """Draw plasma using sliding windows."""
        assert self.canvas is not None

        # Calculate sliding window positions (matches Swift)
        x1 = int(self.hw + self.hw * math.cos(self.count / 97.0 / self.slowness))
        x2 = int(self.hw + self.hw * math.sin(-self.count / 114.0 / self.slowness))
        x3 = int(self.hw + self.hw * math.sin(-self.count / 137.0 / self.slowness))

        y1 = int(self.hh + self.hh * math.sin(self.count / 123.0 / self.slowness))
        y2 = int(self.hh + self.hh * math.cos(-self.count / 75.0 / self.slowness))
        y3 = int(self.hh + self.hh * math.cos(-self.count / 108.0 / self.slowness))

        # Sample plasma and find min/max
        self.lowest_value = 100.0
        self.highest_value = -100.0
        pixel_buffer = []

        for y in range(self.canvas.height):
            row = []
            for x in range(self.canvas.width):
                # Clamp indices to lookup table bounds
                idx1_x = self._clamp(x1 + self.lookup_quant * x, 0, self.plasma_width - 1)
                idx1_y = self._clamp(y1 + self.lookup_quant * y, 0, self.plasma_height - 1)
                idx2_x = self._clamp(x2 + self.lookup_quant * x, 0, self.plasma_width - 1)
                idx2_y = self._clamp(y2 + self.lookup_quant * y, 0, self.plasma_height - 1)
                idx3_x = self._clamp(x3 + self.lookup_quant * x, 0, self.plasma_width - 1)
                idx3_y = self._clamp(y3 + self.lookup_quant * y, 0, self.plasma_height - 1)

                # Sum three sampled values
                value = (self.plasma1[idx1_y][idx1_x] +
                        self.plasma2[idx2_y][idx2_x] +
                        self.plasma2[idx3_y][idx3_x])

                if value < self.lowest_value:
                    self.lowest_value = value
                if value > self.highest_value:
                    self.highest_value = value

                row.append(value)
            pixel_buffer.append(row)

        # Normalize and map to palette
        value_range = max(self.highest_value - self.lowest_value, 0.001)
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                normalized = (pixel_buffer[y][x] - self.lowest_value) / value_range
                palette_idx = min(int(round(normalized * 255)), 255)
                self.canvas.set_pixel(x, y, self.palette[palette_idx])



if __name__ == "__main__":
    run_demo(PlasmaDemo)
