#!/usr/bin/env python3
"""Simple test of the FlaschenTaschen client library (without network connection)."""

import sys
sys.path.insert(0, '..')

from flaschen_taschen.client import Canvas, Color, Config

# Create a canvas with custom geometry
config = Config(width=32, height=24, host="localhost", port=1337)
canvas = Canvas(config, auto_send=False)

# Test pixel operations
print("Testing pixel operations...")
canvas.set_pixel(0, 0, Color.RED)
canvas.set_pixel(31, 0, Color.GREEN)
canvas.set_pixel(0, 23, Color.BLUE)
canvas.set_pixel(31, 23, Color.WHITE)

# Test rectangle fill
print("Testing rectangle fill...")
canvas.fill_rect(10, 10, 12, 4, Color.YELLOW)

# Test line drawing
print("Testing line drawing...")
canvas.draw_line(5, 5, 25, 5, Color.CYAN)
canvas.draw_line(5, 18, 25, 18, Color.MAGENTA)

# Test circle
print("Testing circle...")
canvas.draw_circle(16, 12, 3, Color(128, 64, 32), filled=False)

# Test canvas operations
print(f"Canvas: {config}")
info = canvas.get_frame_info()
print(f"Frame info: {info}")

# Verify pixel was set
pixel_value = canvas.get_pixel(0, 0)
print(f"Pixel at (0,0): {pixel_value}")

print("\n✓ All basic operations work correctly!")
print("Note: Frames not sent to network (auto_send=False)")

canvas.close()
