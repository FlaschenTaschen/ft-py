# Creating Custom Demos

Learn how to create your own interactive animation for the FlaschenTaschen display.

## Demo Structure

A demo is a Python class that extends the `Demo` base class and implements the animation loop.

```python
from flaschen_taschen.demos import Demo
from flaschen_taschen.client import Color

class MyDemo(Demo):
    def setup(self):
        """Called once at startup. Initialize resources."""
        super().setup()  # Always call super first!
        # Add your initialization here
        self.x = 22
        self.y = 17

    def update(self):
        """Called every frame. Update state."""
        self.x += 1
        if self.x >= self.canvas.width:
            self.x = 0

    def draw(self):
        """Called every frame. Render to canvas."""
        self.canvas.clear()
        self.canvas.set_pixel(int(self.x), int(self.y), Color.RED)
```

## Step-by-Step Example: Bouncing Ball

### 1. Create the file

```bash
# Create a new demo file
nano flaschen_taschen/demos/bounce.py
```

### 2. Implement the Demo class

```python
"""Bouncing ball demo."""

import math
from flaschen_taschen.demos import Demo
from flaschen_taschen.client import Color


class BounceBall(Demo):
    """A ball bouncing around the screen with gravity."""

    def setup(self):
        """Initialize the ball position and physics."""
        super().setup()

        # Position
        self.x = self.canvas.width / 2
        self.y = self.canvas.height / 2

        # Velocity
        self.vx = 2.0
        self.vy = 1.0

        # Physics
        self.gravity = 0.2
        self.bounce_damping = 0.8  # Lose energy on bounce

    def update(self):
        """Update position with gravity and bouncing."""
        # Apply gravity
        self.vy += self.gravity

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Bounce off edges
        if self.x <= 2:
            self.x = 2
            self.vx = -self.vx * self.bounce_damping
        elif self.x >= self.canvas.width - 2:
            self.x = self.canvas.width - 2
            self.vx = -self.vx * self.bounce_damping

        if self.y <= 2:
            self.y = 2
            self.vy = -self.vy * self.bounce_damping
        elif self.y >= self.canvas.height - 2:
            self.y = self.canvas.height - 2
            self.vy = -self.vy * self.bounce_damping

    def draw(self):
        """Draw the ball."""
        self.canvas.clear()

        # Draw ball (3-pixel radius circle)
        color = Color(
            int((math.sin(self.frame / 20) + 1) * 127),  # Red oscillates
            int((math.cos(self.frame / 25) + 1) * 127),  # Green oscillates
            int((math.sin(self.frame / 30 + 1) + 1) * 127)  # Blue oscillates
        )
        self.canvas.draw_circle(int(self.x), int(self.y), 3, color, filled=True)
```

### 3. Test locally

```bash
# Run the demo
python -m flaschen_taschen.demos.bounce -t 10

# Or with options
python -m flaschen_taschen.demos.bounce -g 45x35 -h display.local -t 30
```

## Key Patterns

### Accessing Display Dimensions

```python
def draw(self):
    width = self.canvas.width
    height = self.canvas.height
    center_x = width // 2
    center_y = height // 2
```

### Color Cycling

```python
from flaschen_taschen.client import create_hsv_palette

def setup(self):
    super().setup()
    self.palette = create_hsv_palette(256)

def draw(self):
    color = self.palette.get_color(self.frame)
    self.canvas.fill(color)
```

### Frame Counter

```python
def draw(self):
    # self.frame is incremented each draw() call
    x = (self.frame // 5) % self.canvas.width
    self.canvas.set_pixel(x, 10, Color.CYAN)
```

### FPS Measurement

```python
def draw(self):
    # Access current FPS
    fps = self.fps
    # self.fps is calculated from send() times
```

### Random Numbers

```python
import random

def update(self):
    # Standard Python random module works
    x = random.randint(0, self.canvas.width - 1)
    y = random.randint(0, self.canvas.height - 1)
    self.random_pos = (x, y)
```

### Input Parameters from Command Line

```python
def setup(self):
    super().setup()

    # StandardOptions are available via self.std_opts
    delay_ms = self.std_opts.delay
    timeout_s = self.std_opts.timeout
    geometry = (self.std_opts.width, self.std_opts.height)
```

## Common Demo Types

### Particle System

```python
class ParticleDemo(Demo):
    def setup(self):
        super().setup()
        self.particles = []

    def update(self):
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            # Remove dead particles
            if p['life'] > 0:
                p['life'] -= 1
        self.particles = [p for p in self.particles if p['life'] > 0]

        # Spawn new particle
        if len(self.particles) < 10:
            self.particles.append({
                'x': self.canvas.width // 2,
                'y': self.canvas.height // 2,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'life': 50
            })

    def draw(self):
        self.canvas.clear()
        for p in self.particles:
            brightness = int((p['life'] / 50) * 255)
            color = Color(brightness, brightness, brightness)
            self.canvas.set_pixel(int(p['x']), int(p['y']), color)
```

### Grid-Based Simulation

```python
class GridDemo(Demo):
    def setup(self):
        super().setup()
        # Create a grid of cells
        self.grid = [[0 for _ in range(self.canvas.width)]
                     for _ in range(self.canvas.height)]

    def update(self):
        # Update based on neighbors, etc.
        new_grid = [[0 for _ in range(self.canvas.width)]
                    for _ in range(self.canvas.height)]

        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                # Your simulation logic here
                new_grid[y][x] = self.grid[y][x]

        self.grid = new_grid

    def draw(self):
        self.canvas.clear()
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                if self.grid[y][x]:
                    self.canvas.set_pixel(x, y, Color.GREEN)
```

### Mathematical Pattern

```python
import math

class MathDemo(Demo):
    def draw(self):
        self.canvas.clear()

        for x in range(self.canvas.width):
            # Sine wave
            y = int(self.canvas.height / 2 +
                   math.sin(x / 5 + self.frame / 10) * self.canvas.height / 4)

            if 0 <= y < self.canvas.height:
                color = self.palette.get_color(x + self.frame)
                self.canvas.set_pixel(x, y, color)
```

## Testing Your Demo

```bash
# Quick test (5 seconds, localhost)
python -m flaschen_taschen.demos.bounce -t 5

# Test with geometry
python -m flaschen_taschen.demos.bounce -g 45x35 -t 10

# Test with host
python -m flaschen_taschen.demos.bounce -h display.local -t 10

# Test with all options
python -m flaschen_taschen.demos.bounce -g 45x35 -h display.local -d 50 -t 30
```

## Performance Tips

1. **Cache calculations** — Don't recalculate values in `draw()` that were already calculated in `update()`
2. **Minimize canvas.send() calls** — Only call once per frame (automatic with Demo framework)
3. **Use integer arithmetic** — Avoid floats when possible
4. **Limit iterations** — Don't loop over every pixel if you don't need to
5. **Optional numpy** — For math-heavy demos, consider using numpy with try/except fallback

```python
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def fast_math_operation():
    if HAS_NUMPY:
        # numpy version (faster)
        return np.sin(np.linspace(0, 2*np.pi, 256))
    else:
        # pure python fallback
        return [math.sin(i * 2 * math.pi / 256) for i in range(256)]
```

## Documentation

Add a docstring to your demo class:

```python
class MyAwesomeDemo(Demo):
    """
    A really cool animation that does something awesome.

    Features:
    - Multiple colors
    - Smooth motion
    - Gravity physics

    Usage:
        python -m flaschen_taschen.demos.my_awesome_demo -t 30
    """
```

## Next Steps

- Join the [Noisebridge community](https://noisebridge.net) to share your demos
- Check out existing demos in `flaschen_taschen/demos/` for more patterns
- Read [Performance Tuning](performance.md) for optimization techniques
