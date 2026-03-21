# Demos API Reference

## Demo Framework

The `Demo` base class provides a structure for building interactive animations.

### Demo Base Class

```python
from flaschen_taschen.demos import Demo
from flaschen_taschen.standard_options import StandardOptions

class MyDemo(Demo):
    def update(self):
        """Update state for this frame."""
        self.frame += 1

    def draw(self):
        """Draw to the canvas."""
        self.canvas.set_pixel(10, 10, Color.RED)
```

### Lifecycle

1. `setup()` — Called once at start. Initialize canvas, resources.
2. `update()` — Called each frame. Update animation state.
3. `draw()` — Called each frame. Draw to canvas.
4. `send()` — Called each frame. Send canvas to display.
5. `cleanup()` — Called on exit. Close connections.

### Constructor

```python
Demo(std_opts: StandardOptions)
```

- `std_opts` — Standard options (host, geometry, layer, delay, timeout)

### Properties

```python
demo.canvas        # Canvas instance
demo.frame         # Frame counter
demo.fps           # Frames per second
```

### Methods

```python
demo.setup()       # Initialize (called automatically)
demo.update()      # Update state (override this)
demo.draw()        # Render frame (override this)
demo.send()        # Send to display
demo.cleanup()     # Cleanup resources
demo.run()         # Execute the demo (handles loop + timeout)
```

### Example

```python
from flaschen_taschen.demos import Demo
from flaschen_taschen.client import Color

class BouncingBall(Demo):
    def setup(self):
        super().setup()
        self.x = 22
        self.y = 17
        self.vx = 1
        self.vy = 1

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Bounce off edges
        if self.x <= 0 or self.x >= self.canvas.width - 1:
            self.vx = -self.vx
        if self.y <= 0 or self.y >= self.canvas.height - 1:
            self.vy = -self.vy

    def draw(self):
        self.canvas.clear()
        self.canvas.draw_circle(int(self.x), int(self.y), 3, Color.RED)

# Run it
if __name__ == "__main__":
    from flaschen_taschen.demos import run_demo
    run_demo(BouncingBall)
```

### run_demo() Helper

```python
from flaschen_taschen.demos import run_demo

run_demo(MyDemoClass, args=["-g", "45x35", "-t", "30"])
```

Automatically:
- Parses command-line arguments
- Creates StandardOptions
- Instantiates the demo
- Runs the demo loop
- Handles cleanup

---

## Built-in Demos

All 16 demos can be run from the command line:

```bash
python -m flaschen_taschen.demos.<name> [options]
```

| Demo | Module | Description | Notable Flags |
|------|--------|-------------|---------------|
| **Life** | `life` | Conway's Game of Life with toroidal wrapping | `-r` (respawn), `-c`, `-b` (colors) |
| **Maze** | `maze` | Procedural maze generation (depth-first search) | `-c`, `-v`, `-b` (colors) |
| **Sierpinski** | `sierpinski` | Sierpinski triangle (chaos game) | `-c`, `-b` (colors) |
| **Plasma** | `plasma` | Smooth plasma effect | None |
| **Matrix** | `matrix` | Matrix-style falling characters | None |
| **Firefly** | `firefly` | Wandering particles with trails | None |
| **Blur** | `blur` | Shape drawing with blur filter | `-p` (palette), shape type |
| **Quilt** | `quilt` | Procedural quilt pattern | None |
| **Lines** | `lines` | Animated lines with color transitions | `-m` (draw mode) |
| **Fractal** | `fractal` | Mandelbrot set with zoom animation | None |
| **Random Dots** | `random_dots` | Random colored dots at random positions | None |
| **Hack** | `hack` | Rotating 3D text with blur | `-p` (palette), custom text |
| **NbLogo** | `nblogo` | Noisebridge logo bouncing | `-c` (color) |
| **SfLogo** | `sflogo` | Sequoia Fabrica tree logo bouncing | `-c` (color) |
| **Simple Example** | `simple_example` | Static colored rectangles | None |
| **Simple Animation** | `simple_animation` | Animated moving circles | None |

### Running Demos

```bash
# Basic: run for default timeout
python -m flaschen_taschen.demos.plasma

# With geometry
python -m flaschen_taschen.demos.life -g 45x35 -t 30

# With custom host
python -m flaschen_taschen.demos.sierpinski -h display.local -t 10

# With layer
python -m flaschen_taschen.demos.matrix -l 5

# With frame delay
python -m flaschen_taschen.demos.firefly -d 50

# Multiple options
python -m flaschen_taschen.demos.hack -g 45x35 -h display.local -t 60 "HELLO"
```

### Example: Life Demo

```bash
# Run for 30 seconds at default geometry
python -m flaschen_taschen.demos.life -t 30

# With respawn (cleared grid every 100 generations)
python -m flaschen_taschen.demos.life -r -t 60

# Custom colors
python -m flaschen_taschen.demos.life -c ff00ff -b 000000 -t 30
```

### Example: Maze Demo

```bash
# Run maze generation
python -m flaschen_taschen.demos.maze -t 20

# Custom colors (foreground, visited, background)
python -m flaschen_taschen.demos.maze -c ffff00 -v 00ff00 -b 000011 -t 20
```

### Example: Hack Demo (3D Text)

```bash
# Default text "HACK"
python -m flaschen_taschen.demos.hack -t 30

# Custom text
python -m flaschen_taschen.demos.hack "HELLO WORLD" -t 30

# Different palette
python -m flaschen_taschen.demos.hack "CODE" -p 5 -t 30
```
