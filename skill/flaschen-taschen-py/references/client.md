# Client API Reference

Core classes for connecting to the display and drawing content.

## Canvas

The main class for drawing pixels and shapes to the display.

### Creating a Canvas

```python
from flaschen_taschen.client import Canvas, Config

# Simple: use defaults
canvas = Canvas(geometry="45x35", host="display.local")

# Explicit: use Config object
config = Config(geometry="45x35", host="display.local", delay=0)
canvas = Canvas(config=config, auto_send=True)

# Context manager (auto-cleanup)
with Canvas(geometry="45x35", host="display.local") as canvas:
    canvas.set_pixel(22, 17, Color.RED)
    canvas.send()
```

### Constructor

```python
Canvas(config=None, auto_send=True)
```

- `config` (Config): Display configuration. If None, creates a default Config.
- `auto_send` (bool): If True, automatically sends frames after drawing. If False, call `send()` manually.

### Properties

```python
canvas.width       # int: Display width in pixels
canvas.height      # int: Display height in pixels
canvas.fps         # float: Frames per second (calculated from previous sends)
```

### Drawing Methods

#### Pixel-Level

```python
canvas.set_pixel(x, y, color)              # Set a single pixel
canvas.get_pixel(x, y) -> Color | None     # Get a pixel's color
canvas.clear(color=None)                   # Clear entire canvas (to black or specified color)
canvas.fill(color)                         # Alias for clear()
```

#### Shapes

```python
canvas.fill_rect(x, y, width, height, color)        # Filled rectangle
canvas.draw_line(x1, y1, x2, y2, color)             # Line (Bresenham)
canvas.draw_circle(cx, cy, radius, color, filled=False)  # Circle or filled circle
```

### Sending to Display

```python
canvas.send(force=False) -> bool           # Send current frame to display
canvas.flush()                              # Alias for send()
canvas.get_frame_info() -> dict             # Frame timing info (frame_count, fps)
canvas.close()                              # Close connection
```

### Examples

```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")

# Draw and send
canvas.set_pixel(10, 10, Color.RED)
canvas.draw_rect(20, 20, 15, 10, Color.GREEN)
canvas.draw_circle(30, 25, 5, Color.BLUE)
canvas.send()

# Get frame info
info = canvas.get_frame_info()
print(f"Frame {info['frame_count']}: {info['fps']:.1f} FPS")

# Animation loop
for frame in range(100):
    canvas.clear()
    canvas.set_pixel(10 + frame, 10, Color.CYAN)
    canvas.send()

canvas.close()
```

---

## Color

Represents an RGB color.

### Creating Colors

```python
from flaschen_taschen.client import Color

# RGB values (0-255)
red = Color(255, 0, 0)

# Tuple unpacking
color = Color((255, 128, 0))

# Copy existing color
color2 = Color(color)

# Hex string
hex_color = Color.from_hex("#FF8000")
hex_color = Color.from_hex("ff8000")
```

### Named Constants

```python
Color.BLACK        # (0, 0, 0)
Color.WHITE        # (255, 255, 255)
Color.RED          # (255, 0, 0)
Color.GREEN        # (0, 255, 0)
Color.BLUE         # (0, 0, 255)
Color.CYAN         # (0, 255, 255)
Color.MAGENTA      # (255, 0, 255)
Color.YELLOW       # (255, 255, 0)
```

### Methods

```python
color.to_hex() -> str           # Convert to hex: "#FF8000"
color.to_tuple() -> tuple       # Convert to tuple: (255, 128, 0)
color.r, color.g, color.b       # Access individual channels
```

### Examples

```python
# Draw with different colors
canvas.set_pixel(10, 10, Color.RED)
canvas.fill_rect(20, 20, 10, 10, Color.from_hex("#00FF00"))
canvas.draw_circle(30, 30, 5, Color(100, 100, 255))
```

---

## ColorPalette

A list of colors that wraps around when indexed beyond the list size.

### Creating a Palette

```python
from flaschen_taschen.client import ColorPalette, create_hsv_palette, Color

# From list of colors
palette = ColorPalette([Color.RED, Color.GREEN, Color.BLUE])

# Pre-built rainbow palette
palette = ColorPalette(create_hsv_palette(256))

# Predefined palettes
from flaschen_taschen.client import PALETTE_RAINBOW, PALETTE_GRAYSCALE
palette = PALETTE_RAINBOW
```

### Methods

```python
palette.get_color(index) -> Color      # Get color at index (wraps around)
color = palette[index]                 # Alias: palette[0], palette[999]
len(palette)                           # Number of colors in palette
```

### Examples

```python
# Cycle through colors
palette = ColorPalette(create_hsv_palette(256))

for frame in range(1000):
    color = palette.get_color(frame)
    canvas.fill(color)
    canvas.send()
```

---

## Config

Display configuration.

### Constructor

```python
from flaschen_taschen.client import Config

config = Config(
    geometry="45x35+0+0",      # WxH[+X+Y] format, defaults to 45x35
    host="display.local",      # hostname or IP
    port=1337,                 # UDP port
    delay=0,                   # frame delay in ms
    timeout=5.0,               # connection timeout in seconds
    layer=0,                   # display layer (0-15)
)
```

### Class Constants

```python
Config.DEFAULT_WIDTH          # 45
Config.DEFAULT_HEIGHT         # 35
Config.DEFAULT_HOST           # "localhost"
Config.DEFAULT_PORT           # 1337
Config.DEFAULT_FRAME_DELAY_MS # 33
Config.DEFAULT_TIMEOUT_SECONDS # 5
Config.MIN_LAYER              # 0
Config.MAX_LAYER              # 15
```

### Properties

```python
config.width, config.height    # Display dimensions
config.x_offset, config.y_offset  # Offsets
config.host, config.port       # Connection details
config.delay, config.timeout   # Timing
config.layer                   # Active layer
```

### Methods

```python
config.validate()              # Validate configuration (raises ValueError if invalid)
```

### Examples

```python
# Parse geometry string
config = Config(geometry="45x35+10+5")  # 45x35 at offset (10, 5)

# Custom host
config = Config(host="192.168.1.100", port=1337)

# Layer configuration
config = Config(layer=5)  # Use layer 5 instead of 0
```

---

## LayeredCanvas

Manage 16 layers of content independently.

### Creating a LayeredCanvas

```python
from flaschen_taschen.client import LayeredCanvas, Config

config = Config(geometry="45x35")
layered = LayeredCanvas(config=config)
```

### Methods

```python
canvas = layered.get_layer_canvas(layer) -> Canvas  # Get canvas for specific layer
layered.send_layer(layer, pixels) -> bool           # Send specific layer
layered.close()                                      # Close all connections
```

### Examples

```python
layered = LayeredCanvas(config=Config(geometry="45x35"))

# Layer 0: background (red)
canvas0 = layered.get_layer_canvas(0)
canvas0.fill(Color.RED)
canvas0.send()

# Layer 1: overlay (green circle)
canvas1 = layered.get_layer_canvas(1)
canvas1.draw_circle(22, 17, 10, Color.GREEN)
canvas1.send()

layered.close()
```

---

## UDPClient & DisplayConnection

Low-level networking classes (rarely used directly).

### UDPClient

Raw UDP socket communication.

```python
from flaschen_taschen.client import UDPClient, Config

client = UDPClient(config=Config(host="display.local"))
client.send_data(bytes)  # Send raw bytes
client.close()
```

### DisplayConnection

Rate-limited connection wrapper.

```python
from flaschen_taschen.client import DisplayConnection, PPMFormatter, Config

conn = DisplayConnection(config=Config(host="display.local"))
pixels = PPMFormatter.encode([[...], ...])
conn.send_frame(pixels)  # Respects frame delay
conn.close()
```
