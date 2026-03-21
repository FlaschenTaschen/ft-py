---
name: flaschen-taschen-py
description: Create interactive LED display demos using the FlaschenTaschen Python library with 3 clients and 9+ built-in demos.
license: MIT
metadata:
  author: Noisebridge
  version: "1.0"
---

Create interactive LED display animations for the FlaschenTaschen display.

------------------------------------------------------------------------

## Description

This skill helps you build custom demos and animations for the FlaschenTaschen collaborative LED display at Noisebridge. It covers the complete workflow: installing the library, understanding the demo framework (setup/update/draw lifecycle), writing animations, and deploying to the display.

The library supports 3 client types (UDP, Canvas, Generators) and includes 9+ built-in demo templates for inspiration.

**When to use:** When creating new FT demos, optimizing animation performance, or learning the framework.

------------------------------------------------------------------------

## Instructions

1. **Install the Library**
   ```bash
   pip install flaschen-taschen-py
   pip install flaschen-taschen-py[image,video,numpy]  # With all features
   ```

2. **Create Your Demo Class**
   - Extend the `Demo` base class
   - Implement `setup()` for initialization
   - Implement `update()` for state changes each frame
   - Implement `draw()` for rendering

3. **Access the Canvas**
   - Draw pixels: `self.canvas.set_pixel(x, y, color)`
   - Draw shapes: `draw_rect()`, `draw_circle()`, `draw_line()`
   - Clear: `self.canvas.clear()`
   - Display dimensions: `self.canvas.width`, `self.canvas.height`

4. **Use Colors**
   - Named colors: `Color.RED`, `Color.BLUE`, `Color.GREEN`
   - Custom RGB: `Color(255, 128, 0)`
   - Palettes: `create_hsv_palette(256)`

5. **Run and Test**
   ```bash
   python my_demo.py -g 45x35 -h localhost -t 30
   ```
   Options: `-g` (geometry), `-h` (host), `-l` (layer), `-d` (delay), `-t` (timeout)

------------------------------------------------------------------------

## Examples

### Basic Animation

```python
from flaschen_taschen.demos import Demo
from flaschen_taschen.client import Color

class MyDemo(Demo):
    def setup(self):
        super().setup()
        self.x = self.canvas.width // 2

    def update(self):
        self.x += 1
        if self.x >= self.canvas.width:
            self.x = 0

    def draw(self):
        self.canvas.clear()
        self.canvas.set_pixel(self.x, 17, Color.RED)

if __name__ == "__main__":
    from flaschen_taschen.demos import run_demo
    run_demo(MyDemo)
```

### Color Cycling Pattern

```python
def setup(self):
    super().setup()
    from flaschen_taschen.client import create_hsv_palette
    self.palette = create_hsv_palette(256)

def draw(self):
    color = self.palette.get_color(self.frame % 256)
    self.canvas.fill(color)
```

### Physics Example

```python
def setup(self):
    super().setup()
    self.y, self.vy = 0, 1
    self.gravity = 0.2

def update(self):
    self.vy += self.gravity
    self.y += self.vy
    if self.y >= self.canvas.height:
        self.y = self.canvas.height - 1
        self.vy = -self.vy * 0.8
```

------------------------------------------------------------------------

## Best Practices

- **Cache calculations** — Avoid redundant math in the draw loop
- **Use frame counter** — `self.frame` increments each draw call
- **Check performance** — Access `self.fps` to measure framerate
- **Handle optional deps** — Use try/except for numpy/PIL fallbacks
- **Test locally first** — Run without `-h` to use localhost server
- **Inspect built-in demos** — See `flaschen_taschen/demos/` for patterns

------------------------------------------------------------------------

## Key Classes

| Class | Purpose |
|-------|---------|
| `Canvas` | Pixel drawing, primitives (lines, rectangles, circles) |
| `Color` | RGB colors with named constants |
| `Demo` | Base class with setup/update/draw/send lifecycle |
| `StandardOptions` | Command-line parsing (geometry, host, layer, timing) |

------------------------------------------------------------------------

## References

- **[Getting Started](references/getting-started.md)** — Installation, connection setup
- **[Custom Demos Guide](references/custom-demos.md)** — Step-by-step walkthroughs
- **[Demos API](references/demos.md)** — Framework documentation
- **[Client API](references/client.md)** — Canvas and drawing methods
- **[Generators API](references/generators.md)** — Text, image, video rendering
- **[CLI Tools](references/cli.md)** — Command-line utilities
- **[Performance Tuning](references/performance.md)** — Optimization tips
- **[Cookbook](references/cookbook.md)** — Copy-paste recipes

------------------------------------------------------------------------

## Built-in Demos

Explore these demos for patterns and inspiration:

```bash
python -m flaschen_taschen.demos.life       # Conway's Game of Life
python -m flaschen_taschen.demos.plasma     # Plasma effect
python -m flaschen_taschen.demos.sierpinski # Fractal triangle
python -m flaschen_taschen.demos.matrix     # Matrix rain
python -m flaschen_taschen.demos.maze       # Maze generation
```

------------------------------------------------------------------------

## Resources

- [Noisebridge FlaschenTaschen](https://noisebridge.net/wiki/Flaschen_Taschen)
- [PyPI: flaschen-taschen-py](https://pypi.org/project/flaschen-taschen-py/)
- [GitHub: ft-py](https://github.com/FlaschenTaschen/ft-py)
