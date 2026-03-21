"""Firefly demo: Multiple animated light patterns.

Supports 8 different patterns: firefly, rainbow, wave, bounce, twinkle, pulse, chase, matrix.
Pure Python, minimal CPU overhead for RPi compatibility.
"""

import argparse
import math
import random
from enum import Enum
from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo, run_demo


class Pattern(Enum):
    """Available firefly patterns."""
    FIREFLY = "firefly"
    RAINBOW = "rainbow"
    WAVE = "wave"
    BOUNCE = "bounce"
    TWINKLE = "twinkle"
    PULSE = "pulse"
    CHASE = "chase"
    MATRIX = "matrix"


def hsv_to_rgb(hue: int, saturation: int, brightness: int) -> Color:
    """Convert HSV to RGB color.

    Args:
        hue: 0-359
        saturation: 0-255
        brightness: 0-255
    """
    if saturation == 0:
        return Color(brightness, brightness, brightness)

    base = ((255 - saturation) * brightness) >> 8
    hue_segment = hue // 60
    hue_remainder = hue % 60
    val = brightness
    r = val - base

    if hue_segment == 0:
        g = (r * hue_remainder) // 60 + base
        return Color(val, g, base)
    elif hue_segment == 1:
        r_comp = (r * (60 - hue_remainder)) // 60 + base
        return Color(r_comp, val, base)
    elif hue_segment == 2:
        b = (r * hue_remainder) // 60 + base
        return Color(base, val, b)
    elif hue_segment == 3:
        g_comp = (r * (60 - hue_remainder)) // 60 + base
        return Color(base, g_comp, val)
    elif hue_segment == 4:
        r_comp = (r * hue_remainder) // 60 + base
        return Color(r_comp, base, val)
    else:  # hue_segment == 5
        g_comp = (r * (60 - hue_remainder)) // 60 + base
        return Color(val, base, g_comp)


class Firefly:
    """A single pulsing firefly light."""

    def __init__(self, x: float, y: float, width: int, height: int, hue: int, vx: float, vy: float):
        """Initialize firefly at position.

        Args:
            x: Starting X position
            y: Starting Y position
            width: Canvas width
            height: Canvas height
            hue: Color hue (0-359)
            vx: X velocity
            vy: Y velocity
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = width
        self.height = height
        self.hue = hue
        self.glow_counter = 0

    def update(self) -> None:
        """Update firefly position and glow."""
        self.glow_counter += 1

        # Move slowly
        self.x += self.vx
        self.y += self.vy

        # Wrap around edges
        if self.x < 0:
            self.x += self.width
        if self.x >= self.width:
            self.x -= self.width
        if self.y < 0:
            self.y += self.height
        if self.y >= self.height:
            self.y -= self.height

    def get_position(self) -> tuple[int, int]:
        """Get current integer position."""
        return (int(self.x), int(self.y))

    def get_color(self) -> Color:
        """Get pulsing firefly color."""
        sine_value = math.sin((2 * math.pi / 30) * self.glow_counter) * 127.5 + 127.5
        brightness = max(0, min(255, int(sine_value)))
        return hsv_to_rgb(self.hue, 255, brightness)


class BouncingLight:
    """A bouncing light (for bounce pattern)."""

    def __init__(self, x: float, y: float, width: int, height: int, hue: int, vx: float, vy: float):
        """Initialize bouncing light."""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = width
        self.height = height
        self.hue = hue

    def update(self) -> None:
        """Update position with bouncing."""
        self.x += self.vx
        self.y += self.vy

        # Bounce off edges
        if self.x <= 0 or self.x >= self.width - 1:
            self.vx = -self.vx
            self.x = max(0, min(self.width - 1, self.x))
        if self.y <= 0 or self.y >= self.height - 1:
            self.vy = -self.vy
            self.y = max(0, min(self.height - 1, self.y))

    def get_color(self, brightness: int) -> Color:
        """Get color with given brightness."""
        return hsv_to_rgb(self.hue, 255, brightness)


class FireflyDemo(Demo):
    """Firefly demo with multiple patterns."""

    def setup(self) -> None:
        """Initialize fireflies."""
        super().setup()
        assert self.canvas is not None

        # Parse pattern option
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-p", "--pattern",
            default="firefly",
            help="Pattern: firefly, rainbow, wave, bounce, twinkle, pulse, chase, matrix"
        )
        demo_args, _ = parser.parse_known_args(self.std_opts.non_standard_args)

        try:
            self.pattern = Pattern(demo_args.pattern)
        except ValueError:
            self.pattern = Pattern.FIREFLY

        self.num_lights = 5
        self.fireflies = []
        self.bouncing_lights = []
        self.frame_count = 0
        self.rainbow_offset = 0
        self.wave_offset = 0
        self.twinkle_frame = 0
        self.chase_offset = 0

        self._init_fireflies()
        if self.pattern == Pattern.BOUNCE:
            self._init_bouncing()

    def _init_fireflies(self) -> None:
        """Initialize fireflies."""
        self.fireflies = []
        for i in range(self.num_lights):
            assert self.canvas is not None
            x = random.uniform(0, self.canvas.width)
            y = random.uniform(0, self.canvas.height)
            vx = random.uniform(-0.05, 0.05)
            vy = random.uniform(-0.05, 0.05)
            hue = int((359 / self.num_lights) * i)
            firefly = Firefly(x, y, self.canvas.width, self.canvas.height, hue, vx, vy)
            self.fireflies.append(firefly)

    def _init_bouncing(self) -> None:
        """Initialize bouncing lights."""
        self.bouncing_lights = []
        assert self.canvas is not None
        for i in range(self.num_lights):
            x = random.uniform(0, self.canvas.width)
            y = random.uniform(0, self.canvas.height)
            vx = random.uniform(-0.1, 0.1)
            vy = random.uniform(-0.1, 0.1)
            hue = int((359 / self.num_lights) * i)
            light = BouncingLight(x, y, self.canvas.width, self.canvas.height, hue, vx, vy)
            self.bouncing_lights.append(light)

    def update(self) -> None:
        """Update all fireflies."""
        self.frame_count += 1

        for firefly in self.fireflies:
            firefly.update()

        if self.pattern == Pattern.BOUNCE:
            for light in self.bouncing_lights:
                light.update()

    def draw(self) -> None:
        """Draw fireflies with current pattern."""
        assert self.canvas is not None

        self.canvas.clear(Color.BLACK)

        match self.pattern:
            case Pattern.FIREFLY:
                self._draw_firefly()
            case Pattern.RAINBOW:
                self._draw_rainbow()
            case Pattern.WAVE:
                self._draw_wave()
            case Pattern.BOUNCE:
                self._draw_bounce()
            case Pattern.TWINKLE:
                self._draw_twinkle()
            case Pattern.PULSE:
                self._draw_pulse()
            case Pattern.CHASE:
                self._draw_chase()
            case Pattern.MATRIX:
                self._draw_matrix()

    def _draw_firefly(self) -> None:
        """Draw glowing pulsing lights."""
        assert self.canvas is not None
        for firefly in self.fireflies:
            x, y = firefly.get_position()
            color = firefly.get_color()
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)

    def _draw_rainbow(self) -> None:
        """Draw cycling rainbow colors."""
        assert self.canvas is not None
        self.rainbow_offset = (self.rainbow_offset + 1) % 256
        for i, firefly in enumerate(self.fireflies):
            x, y = firefly.get_position()
            hue = (self.rainbow_offset + int(i * (360 / self.num_lights))) % 360
            color = hsv_to_rgb(hue, 255, 255)
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)

    def _draw_wave(self) -> None:
        """Draw wave effect."""
        assert self.canvas is not None
        self.wave_offset = (self.wave_offset + 1) % 256
        for firefly in self.fireflies:
            x, y = firefly.get_position()
            wave = math.sin((x + self.wave_offset) * 0.1) * 127.5 + 127.5
            hue = int(wave * 359.0 / 255.0)
            color = hsv_to_rgb(hue, 255, int(wave))
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)

    def _draw_bounce(self) -> None:
        """Draw bouncing lights."""
        assert self.canvas is not None
        for light in self.bouncing_lights:
            brightness = int(math.sin(self.frame_count * 0.05) * 127.5 + 127.5)
            color = light.get_color(brightness)
            x, y = int(light.x), int(light.y)
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)

    def _draw_twinkle(self) -> None:
        """Draw twinkling lights."""
        assert self.canvas is not None
        self.twinkle_frame = (self.twinkle_frame + 1) % 30
        for i, firefly in enumerate(self.fireflies):
            x, y = firefly.get_position()
            brightness = max(0, 255 - ((self.twinkle_frame + i * 3) % 30) * 8)
            hue = int(i * (359 / self.num_lights))
            color = hsv_to_rgb(hue, 255, brightness)
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)

    def _draw_pulse(self) -> None:
        """Draw all lights pulsing together."""
        assert self.canvas is not None
        brightness = int(math.sin(self.frame_count * 0.05) * 127.5 + 127.5)
        for i, firefly in enumerate(self.fireflies):
            x, y = firefly.get_position()
            hue = (self.frame_count // 4 + int(i * (359 / self.num_lights))) % 360
            color = hsv_to_rgb(hue, 255, brightness)
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)

    def _draw_chase(self) -> None:
        """Draw lights chasing each other."""
        assert self.canvas is not None
        self.chase_offset = (self.chase_offset + 1) % 360
        for i, firefly in enumerate(self.fireflies):
            x, y = firefly.get_position()
            angle = (self.chase_offset + int(i * (360 / self.num_lights))) % 360
            brightness = int(math.sin(math.radians(angle)) * 127.5 + 127.5)
            color = hsv_to_rgb(angle, 255, brightness)
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)

    def _draw_matrix(self) -> None:
        """Draw digital rain effect."""
        assert self.canvas is not None
        for i, firefly in enumerate(self.fireflies):
            x, y = firefly.get_position()
            flicker = (self.frame_count + i * 5) % 20
            brightness = 255 if flicker < 15 else 100
            color = hsv_to_rgb(120, 255, brightness)
            if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
                self.canvas.set_pixel(x, y, color)


if __name__ == "__main__":
    run_demo(FireflyDemo)
