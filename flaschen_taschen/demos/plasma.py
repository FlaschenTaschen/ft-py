"""Plasma demo: Animated plasma effect with sliding lookup tables.

Ported from PlasmaDemo.swift - uses pre-computed lookup tables with
sliding windows to create animated plasma effect. Supports numpy for
optional performance optimization.
"""

import math
import random

from flaschen_taschen.client.color import create_hsv_palette
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

        # Color palette
        palette_obj = create_hsv_palette(256)
        self.palette = palette_obj.colors

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
