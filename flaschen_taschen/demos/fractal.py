"""
Fractal - Mandelbrot set with smooth zoom animation
Ported from fractal.cc and FractalDemo.swift

Renders the Mandelbrot set with smooth zooming in and out of a specific point.
Uses two buffers: one for computation at 2x resolution, one for display.
The color palette animates continuously using trigonometric functions.
"""

import math
from flaschen_taschen.demos import Demo
from flaschen_taschen.client.color import Color
from flaschen_taschen.standard_options import StandardOptions


# Mandelbrot point to zoom into
POINT_OR = -0.577816
POINT_OI = -0.631121


class FractalState:
    """Manages Mandelbrot set computation and display buffers."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Computation buffer (2x resolution): stores iteration counts
        self.fractal1 = [0] * (width * height * 4)
        # Display buffer (same resolution as fractal1)
        self.fractal2 = [0] * (width * height * 4)

        # Computation state
        self.dr = 0.0  # Real step per pixel
        self.di = 0.0  # Imaginary step per pixel
        self.pr = 0.0  # Current real position
        self.pi = 0.0  # Current imaginary position
        self.sr = 0.0  # Start real position
        self.si = 0.0  # Start imaginary position
        self.offset = 0  # Current computation offset

    def start_computation(self, sr, si, er, ei):
        """Start computing Mandelbrot set from sr,si to er,ei."""
        self.dr = (er - sr) / (self.width * 2)
        self.di = (ei - si) / (self.height * 2)
        self.pr = sr
        self.pi = si
        self.sr = sr
        self.si = si
        self.offset = 0

    def compute_lines(self, line_count):
        """Compute line_count lines of the Mandelbrot set."""
        for _ in range(line_count):
            if self.offset >= self.width * self.height * 4:
                return

            self.pr = self.sr
            for _ in range(self.width * 2):
                # Mandelbrot iteration: count how many iterations until |z| > 2
                c = 0
                vr = self.pr
                vi = self.pi

                while (vr * vr + vi * vi < 4.0) and c < 255:
                    nvr = vr * vr - vi * vi + self.pr
                    nvi = 2.0 * vi * vr + self.pi
                    vi = nvi
                    vr = nvr
                    c += 1

                self.fractal1[self.offset] = c
                self.offset += 1
                if self.offset >= self.width * self.height * 4:
                    return
                self.pr += self.dr

            self.pi += self.di

    def swap_buffers(self):
        """Swap computation and display buffers."""
        self.fractal1, self.fractal2 = self.fractal2, self.fractal1

    def zoom_fractal(self, z, pixels):
        """Apply zoom transformation to display pixels using bilinear interpolation."""
        width16 = self.width << 17
        height16 = self.height << 17
        z256 = 256.0 * (1.0 + z)

        width_fix = int((width16 / z256)) << 8
        height_fix = int((height16 / z256)) << 8
        startx = (width16 - width_fix) >> 1
        starty = (height16 - height_fix) >> 1
        deltax = width_fix // self.width
        deltay = height_fix // self.height

        offset = 0
        py = starty

        for _ in range(self.height):
            px = startx
            for _ in range(self.width):
                py_idx = (py >> 16) * (self.width * 2)
                py_frac = (py >> 8) & 0xff
                px_idx = px >> 16
                px_frac = (px >> 8) & 0xff

                # Bilinear interpolation weights
                w1 = (0x100 - py_frac) * (0x100 - px_frac)
                w2 = (0x100 - py_frac) * px_frac
                w3 = py_frac * (0x100 - px_frac)
                w4 = py_frac * px_frac

                # Sample four surrounding pixels
                v1 = self.fractal2[py_idx + px_idx] * w1
                v2 = self.fractal2[py_idx + px_idx + 1] * w2
                v3 = self.fractal2[py_idx + (self.width * 2) + px_idx] * w3
                v4 = self.fractal2[py_idx + (self.width * 2) + px_idx + 1] * w4

                pixels[offset] = (v1 + v2 + v3 + v4) >> 16

                px += deltax
                offset += 1

            py += deltay


class Fractal(Demo):
    """
    Mandelbrot set fractal with smooth zoom animation.

    The demo:
    - Computes Mandelbrot set at 2x resolution for smooth zooming
    - Alternates between zooming in and out every 38 zoom cycles
    - Uses bilinear interpolation for smooth zoom transitions
    - Animates palette with cosine-based color cycling
    """

    def __init__(self, std_opts):
        super().__init__(std_opts)

    def setup(self):
        """Initialize fractal computation and palette."""
        super().setup()

        self.state = FractalState(self.canvas.width, self.canvas.height)
        self.palette = [Color(0, 0, 0) for _ in range(256)]
        self.pixels = [0] * (self.canvas.width * self.canvas.height)

        # Zoom animation state
        self.zx = 4.0
        self.zy = 4.0
        self.zoom_in = True
        self.frame_count = 0
        self.k = 0
        self.compute_step = 0
        self.compute_steps_per_zoom = max(1, self.canvas.height)
        self.needs_new_zoom = True

        # Initial fractal computation
        self.state.start_computation(
            POINT_OR - self.zx, POINT_OI - self.zy,
            POINT_OR + self.zx, POINT_OI + self.zy
        )
        for _ in range(100):
            self.state.compute_lines(2)
        self.state.swap_buffers()

    def update(self):
        """Update fractal computation and zoom state."""
        if self.needs_new_zoom:
            if self.zoom_in:
                self.zx *= 0.5
                self.zy *= 0.5
            else:
                self.zx *= 2.0
                self.zy *= 2.0

            self.state.start_computation(
                POINT_OR - self.zx, POINT_OI - self.zy,
                POINT_OR + self.zx, POINT_OI + self.zy
            )
            self.compute_step = 0
            self.needs_new_zoom = False

        self.state.compute_lines(2)
        self.compute_step += 1

    def draw(self):
        """Draw the fractal with zoom and palette animation."""
        # Calculate zoom factor for smooth transition
        z = self.compute_step / self.compute_steps_per_zoom
        zoom_factor = z if self.zoom_in else (1.0 - z)

        # Apply zoom to get display pixels
        self.state.zoom_fractal(zoom_factor, self.pixels)

        # Update palette
        self._update_palette()

        # Draw pixels to canvas
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                idx = y * self.canvas.width + x
                color = self.palette[self.pixels[idx]]
                self.canvas.set_pixel(x, y, color)

        # Check if zoom cycle complete
        if self.compute_step >= self.compute_steps_per_zoom:
            self.state.swap_buffers()
            self.k += 1
            self.needs_new_zoom = True

            # Toggle zoom direction every 38 cycles
            if self.k % 38 == 0:
                self.zoom_in = not self.zoom_in

        self.frame_count += 1

    def _update_palette(self):
        """Update the 256-color palette using cosine animation."""
        t = float(self.frame_count)
        for i in range(256):
            fi = float(i)
            angle1 = fi * math.pi / 128.0 + t * 0.0212
            angle2 = fi * math.pi / 64.0 + t * 0.0136

            c1 = 128.0 - 127.0 * math.cos(angle1)
            c2 = 128.0 - 127.0 * math.cos(angle2)

            r = int(c2) & 0xFF
            b = int(c1) & 0xFF

            self.palette[i] = Color(r, 0, b)


if __name__ == '__main__':
    from flaschen_taschen.demos import run_demo
    run_demo(Fractal)
