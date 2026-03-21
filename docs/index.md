# FlaschenTaschen Python Documentation

Welcome to the FlaschenTaschen Python library documentation. This library provides a complete client for the Noisebridge FlaschenTaschen LED display.

## What is FlaschenTaschen?

FlaschenTaschen is a large, collaborative LED display installed at Noisebridge. The Python library allows you to:
- Send text, images, and video to the display
- Draw primitives (lines, rectangles, circles)
- Create interactive animations and demos
- Layer multiple content sources
- Access the display from any machine on the network

## Quick Start

**Install:**
```bash
pip install flaschen-taschen-py
```

**First script:**
```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")
canvas.set_pixel(22, 17, Color.RED)
canvas.send()
canvas.cleanup()
```

**Run a demo:**
```bash
python -m flaschen_taschen.demos.plasma -t 10
```

## Documentation Index

| Topic | Purpose |
|-------|---------|
| **[Getting Started](getting-started.md)** | Installation, connection setup, running demos |
| **[Client API](api/client.md)** | Canvas, Color, Config, connection management |
| **[Demos API](api/demos.md)** | Demo framework and all 16 available demos |
| **[Generators API](api/generators.md)** | Text, image, and video rendering |
| **[CLI Tools](api/cli.md)** | Command-line tools reference |
| **[Creating Custom Demos](guides/custom-demos.md)** | How to write your own demo |
| **[Performance Tuning](guides/performance.md)** | Frame rates, geometry, optimization tips |
| **[Code Cookbook](examples/cookbook.md)** | Copy-paste recipes for common tasks |

## Key Concepts

### Canvas
The Canvas class handles pixel-level drawing and sending frames to the display.

```python
canvas = Canvas(geometry="45x35", host="display.local")
canvas.set_pixel(10, 10, Color.BLUE)
canvas.draw_rect(20, 20, 10, 10, Color.GREEN)
canvas.send()
```

### Color
Create colors with RGB values, hex strings, or use named constants.

```python
red = Color.RED
custom = Color(255, 128, 0)
hex_color = Color.from_hex("#FF8000")
```

### Demos
Pre-built animations that demonstrate the library's capabilities.

```bash
python -m flaschen_taschen.demos.life        # Conway's Game of Life
python -m flaschen_taschen.demos.plasma      # Plasma effect
python -m flaschen_taschen.demos.sierpinski  # Sierpinski triangle
```

### Generators
Content generators for text, images, and video.

```python
from flaschen_taschen.generators.text import send_text

send_text(host="display.local", port=1337, geometry="45x35",
          text="Hello World", color=Color.CYAN)
```

## Requirements

- Python 3.8+
- No required external dependencies for core functionality
- Optional: Pillow (images), ffmpeg (video), numpy (performance)

## Getting Help

- Check [Getting Started](getting-started.md) for basic setup
- See [Code Cookbook](examples/cookbook.md) for common patterns
- Browse [API docs](api/client.md) for detailed class references
- Read [Performance Tuning](guides/performance.md) for optimization

## License

MIT
