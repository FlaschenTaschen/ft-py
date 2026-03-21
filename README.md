# FlaschenTaschen Python Client

A Python port of the FlaschenTaschen display control library for the [Noisebridge FlaschenTaschen](https://noisebridge.net/wiki/Flaschen_Taschen) LED display.

## Features

- **UDP Client**: Direct communication with FlaschenTaschen displays
- **Canvas & Drawing**: Pixel-level control with primitive drawing (lines, rectangles, circles)
- **Content Generators**: Text, image, and video rendering to the display
- **Interactive Demos**: 9+ demo animations including Conway's Game of Life, plasma effects, fractals, and more
- **CLI Tools**: Command-line utilities for quick content sending
- **Multi-layer Support**: 16-layer display rendering with compositing

## Installation

### Basic Installation

```bash
pip install flaschen-taschen-py
```

### With Optional Dependencies

For image support:
```bash
pip install flaschen-taschen-py[image]
```

For video support:
```bash
pip install flaschen-taschen-py[video]
```

For numpy optimization (demos):
```bash
pip install flaschen-taschen-py[numpy]
```

For all features:
```bash
pip install flaschen-taschen-py[image,video,numpy]
```

## Quick Start

### Send Text to Display

```bash
send-text -g 45x35 -h display.local "Hello World"
```

### Send Image

```bash
send-image -g 45x35 image.png
```

### Send Video

```bash
send-video -g 45x35 -fps 24 video.mp4
```

### Debug Display

```bash
ft-debugger -m fill -t 10  # Fill screen for 10 seconds
```

## Interactive Demos

Run any of these demos:

```bash
# Classic simulations
python -m flaschen_taschen.demos.life -g 45x35 -t 30          # Conway's Game of Life
python -m flaschen_taschen.demos.maze -g 45x35 -t 30          # Procedural maze generation
python -m flaschen_taschen.demos.sierpinski -g 45x35 -t 30    # Sierpinski triangle

# Generative graphics
python -m flaschen_taschen.demos.plasma -g 45x35              # Plasma effect
python -m flaschen_taschen.demos.matrix -g 45x35              # Matrix rain
python -m flaschen_taschen.demos.firefly -g 45x35             # Wandering particles
python -m flaschen_taschen.demos.blur -g 45x35                # Blur effect

# Advanced effects
python -m flaschen_taschen.demos.fractal -g 45x35             # Mandelbrot zoom
python -m flaschen_taschen.demos.lines -g 45x35               # Animated lines
python -m flaschen_taschen.demos.random_dots -g 45x35         # Random particles
python -m flaschen_taschen.demos.hack -g 45x35                # Rotating 3D text
python -m flaschen_taschen.demos.nblogo -g 45x35              # Noisebridge logo
python -m flaschen_taschen.demos.sflogo -g 45x35              # Sequoia Fabrica logo
```

### Common Demo Options

```bash
-g, --geometry WxH[+X+Y]   Display geometry (default: 45x35)
-h, --host HOSTNAME        Display hostname (default: localhost)
-l, --layer N              Layer number 0-15 (default: 0)
-d, --delay MS             Frame delay in milliseconds (default: 0)
-t, --timeout S            Run for N seconds then exit
```

## Python API

### Basic Example

```python
from flaschen_taschen.client import Canvas, Color
import time

# Connect to display
canvas = Canvas(geometry="45x35", host="display.local")

# Draw and send
canvas.set_pixel(10, 10, Color.RED)
canvas.draw_rect(20, 20, 10, 10, Color.GREEN)
canvas.send()

time.sleep(1)
canvas.cleanup()
```

### Rendering Loop

```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")

for frame in range(100):
    canvas.clear()
    # Draw frame content
    canvas.draw_circle(22, 17, frame % 10, Color.BLUE)
    canvas.send()

canvas.cleanup()
```

## Project Structure

- `flaschen_taschen/` - Main package
  - `client/` - UDP communication, Canvas, Color support
  - `demos/` - Interactive demo animations
  - `generators/` - Text, image, video content generators
  - `cli/` - Command-line tool entry points
  - `utils/` - Bitmap font and utility functions
- `tests/` - Test suite (150+ tests)
- `scripts/` - Shell script wrappers for demos

## Configuration

### Display Connection

```python
from flaschen_taschen.client import Config

config = Config(
    geometry="45x35+10+5",  # Width, height, X offset, Y offset
    host="display.local",
    port=1337,
    delay=0,  # Frame delay in ms
)
```

### Colors

```python
from flaschen_taschen.client import Color

# Named colors
red = Color.RED
blue = Color.BLUE

# RGB values
custom = Color(255, 128, 0)  # Orange

# Hex strings
hex_color = Color.from_hex("#FF8000")
```

## Development

Clone the repository and install with dev dependencies:

```bash
git clone https://github.com/FlaschenTaschen/ft-py.git
cd ft-py
pip install -e ".[dev,image,video,numpy]"
```

Run tests:

```bash
pytest
```

## Requirements

- Python 3.8+
- No required external dependencies for core functionality
- Optional: Pillow (image support), ffmpeg-python (video support), numpy (performance)

## License

MIT

## References

- [FlaschenTaschen Project](https://noisebridge.net/wiki/Flaschen_Taschen)
- [Display Server](https://github.com/hzeller/flaschen-taschen)
