# Code Cookbook

Copy-paste recipes for common tasks.

## Display Text

### Static Text

```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")
canvas.clear()

# Simple static text (requires bitmap font)
from flaschen_taschen.utils.bitmap_font import BitmapFont

text = "HELLO"
x, y = 5, 15
for i, char in enumerate(text):
    bitmap = BitmapFont.render_char(char, scale=1)
    # Draw bitmap to canvas (simplified)

canvas.send()
time.sleep(5)
canvas.close()
```

### Scrolling Text (CLI)

```bash
send-text -h display.local -c 00ff00 -t 30 "Scrolling Message"
```

### Scrolling Text (Python)

```python
from flaschen_taschen.generators.text import TextGenerator
from flaschen_taschen.client import Canvas, Color
import time

canvas = Canvas(geometry="45x35", host="display.local")

gen = TextGenerator(
    canvas=canvas,
    text="Hello World",
    color=Color.GREEN,
    scroll=True,
    scroll_speed=1
)

gen.render_scrolling(y=17, duration=30, frame_rate=30)
canvas.close()
```

---

## Display Images

### Single Image

```python
from flaschen_taschen.generators.image import send_image
from flaschen_taschen.client import Color

send_image(
    host="display.local",
    port=1337,
    geometry="45x35",
    image_path="photo.png",
    timeout_s=10
)
```

### Image on Specific Layer

```bash
send-image -h display.local -l 5 logo.png
```

---

## Draw Shapes

### Rectangles and Circles

```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")
canvas.clear()

# Filled rectangle
canvas.fill_rect(5, 5, 10, 10, Color.RED)

# Filled circle
canvas.draw_circle(22, 17, 8, Color.BLUE, filled=True)

# Circle outline
canvas.draw_circle(30, 25, 5, Color.GREEN, filled=False)

# Line
canvas.draw_line(0, 0, 44, 34, Color.YELLOW)

canvas.send()
time.sleep(5)
canvas.close()
```

### Grid Pattern

```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")
canvas.clear()

# Draw a grid
for x in range(0, canvas.width, 5):
    canvas.draw_line(x, 0, x, canvas.height - 1, Color.CYAN)

for y in range(0, canvas.height, 5):
    canvas.draw_line(0, y, canvas.width - 1, y, Color.CYAN)

canvas.send()
time.sleep(5)
canvas.close()
```

---

## Color Cycling

### Animate Background Color

```python
from flaschen_taschen.client import Canvas, create_hsv_palette

canvas = Canvas(geometry="45x35", host="display.local")
palette = create_hsv_palette(256)

for frame in range(300):
    color = palette.get_color(frame)
    canvas.fill(color)
    canvas.send()

canvas.close()
```

### Multiple Cycling Colors

```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")

for frame in range(300):
    # Create color that shifts over time
    r = int((256 + frame) % 256)
    g = int((256 + frame * 2) % 256)
    b = int((256 + frame * 3) % 256)

    canvas.clear(Color(r, g, b))

    # Draw white text or shapes
    canvas.draw_circle(22, 17, 5, Color.WHITE, filled=True)

    canvas.send()

canvas.close()
```

---

## Simple Animation

### Bouncing Pixel

```python
from flaschen_taschen.client import Canvas, Color
import time

canvas = Canvas(geometry="45x35", host="display.local")

x, y = 22, 17
vx, vy = 1, 1

for frame in range(200):
    canvas.clear()

    # Update position
    x += vx
    y += vy

    # Bounce off edges
    if x <= 0 or x >= canvas.width - 1:
        vx = -vx
    if y <= 0 or y >= canvas.height - 1:
        vy = -vy

    # Draw
    canvas.set_pixel(int(x), int(y), Color.RED)
    canvas.send()

canvas.close()
```

### Expanding Circle

```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")

for frame in range(100):
    canvas.clear()

    radius = (frame % 20)
    canvas.draw_circle(22, 17, radius, Color.GREEN)

    canvas.send()

canvas.close()
```

### Rotating Lines

```python
from flaschen_taschen.client import Canvas, Color
import math

canvas = Canvas(geometry="45x35", host="display.local")

for frame in range(200):
    canvas.clear()

    angle = frame * 3.6 / 100  # Rotate 3.6 degrees per frame
    rad = math.radians(angle)

    # Draw line from center with rotating angle
    cx, cy = canvas.width // 2, canvas.height // 2
    length = 15
    x2 = int(cx + length * math.cos(rad))
    y2 = int(cy + length * math.sin(rad))

    canvas.draw_line(cx, cy, x2, y2, Color.CYAN)
    canvas.send()

canvas.close()
```

---

## Using Layers

### Composite Content

```python
from flaschen_taschen.client import LayeredCanvas, Config, Color

config = Config(geometry="45x35", host="display.local")
layered = LayeredCanvas(config=config)

# Layer 0 (top): White text
canvas0 = layered.get_layer_canvas(0)
canvas0.clear(Color(255, 0, 0))  # Red background
canvas0.send()

# Layer 1 (below): Green circle
canvas1 = layered.get_layer_canvas(1)
canvas1.draw_circle(22, 17, 10, Color.GREEN)
canvas1.send()

import time
time.sleep(5)

layered.close()
```

### Animated Overlay

```python
from flaschen_taschen.client import LayeredCanvas, Config, Color

config = Config(geometry="45x35", host="display.local")
layered = LayeredCanvas(config=config)

# Static background
bg_canvas = layered.get_layer_canvas(1)
bg_canvas.fill(Color(20, 20, 40))  # Dark blue
bg_canvas.send()

# Animated overlay
fg_canvas = layered.get_layer_canvas(0)

for frame in range(200):
    fg_canvas.clear()

    x = 10 + frame % 35
    fg_canvas.set_pixel(x, 17, Color.YELLOW)

    fg_canvas.send()

layered.close()
```

---

## Run a Demo with Code

### Execute Demo Programmatically

```python
from flaschen_taschen.demos.plasma import Plasma
from flaschen_taschen.standard_options import StandardOptions

# Create options
opts = StandardOptions(["-g", "45x35", "-h", "display.local", "-t", "30"])

# Create and run demo
demo = Plasma(opts)
demo.run()
```

### Custom Demo Arguments

```python
from flaschen_taschen.demos import run_demo
from flaschen_taschen.demos.life import Life

# Run with custom args
run_demo(Life, args=["-g", "45x35", "-t", "60", "-r"])
```

---

## Error Handling

### Connection Retry

```python
from flaschen_taschen.client import Canvas, Config
import time

for attempt in range(3):
    try:
        canvas = Canvas(geometry="45x35", host="display.local")
        canvas.set_pixel(10, 10, Color.RED)
        canvas.send()
        canvas.close()
        print("Success!")
        break
    except ConnectionError as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < 2:
            time.sleep(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        break
```

### Graceful Cleanup

```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")

try:
    canvas.set_pixel(22, 17, Color.RED)
    canvas.send()
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    canvas.clear()
    canvas.send()
    canvas.close()
    print("Cleaned up")
```

### Context Manager (Automatic Cleanup)

```python
from flaschen_taschen.client import Canvas, Color

# Automatically closes on exit
with Canvas(geometry="45x35", host="display.local") as canvas:
    canvas.set_pixel(22, 17, Color.RED)
    canvas.send()
    # auto cleanup happens here
```

---

## Performance Optimization

### Pre-Compute Sine Table

```python
import math
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")

# Pre-compute once
sine_table = [math.sin(i * 2 * math.pi / 256) for i in range(256)]

for frame in range(300):
    canvas.clear()

    # Look up instead of computing
    val = sine_table[frame % 256]
    y = int(canvas.height / 2 + val * 10)

    canvas.set_pixel(22, y, Color.GREEN)
    canvas.send()

canvas.close()
```

### Cache Color Palette

```python
from flaschen_taschen.client import Canvas, create_hsv_palette

canvas = Canvas(geometry="45x35", host="display.local")

# Cache palette once
palette = create_hsv_palette(256)

for frame in range(1000):
    color = palette.get_color(frame)  # Fast lookup
    canvas.fill(color)
    canvas.send()

canvas.close()
```

---

## Complete Working Example

```python
"""Complete example combining multiple techniques."""

from flaschen_taschen.client import Canvas, Color, create_hsv_palette
import time
import math

def main():
    canvas = Canvas(geometry="45x35", host="display.local", auto_send=True)

    try:
        # Pre-compute palette
        palette = create_hsv_palette(256)

        # Animation loop
        for frame in range(500):
            canvas.clear()

            # Rotate through colors
            bg_color = palette.get_color(frame)
            canvas.fill(bg_color)

            # Draw bouncing circle
            x = canvas.width / 2 + 10 * math.sin(frame / 20)
            y = canvas.height / 2 + 10 * math.cos(frame / 15)

            canvas.draw_circle(int(x), int(y), 5, Color.WHITE, filled=True)

            # Send frame
            canvas.send()

            # Show FPS periodically
            if frame % 100 == 0:
                print(f"Frame {frame}: {canvas.fps:.1f} FPS")

            # Small delay for readability
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        canvas.clear()
        canvas.send()
        canvas.close()

if __name__ == "__main__":
    main()
```

---

## CLI One-Liners

### Quick Test

```bash
# Flash white and red
ft-debugger -m fill -t 3

# Send red text
send-text -c ff0000 "ERROR"

# Display image
send-image photo.png

# Play video
send-video video.mp4
```

### Chained Commands

```bash
# Clear display, then show text
ft-debugger -m fill -t 1 && send-text "Ready"

# Show image for 10 seconds, then demo
send-image -t 10 logo.png && python -m flaschen_taschen.demos.plasma -t 30
```
