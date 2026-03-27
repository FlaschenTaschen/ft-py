# Performance Tuning Guide

Tips for optimizing frame rates and responsiveness on the display.

## Display Basics

- **Default geometry:** 45x35 pixels (1,575 pixels total)
- **Default frame rate:** 30 FPS (33ms per frame)
- **Network:** UDP on port 1337, ~100 kB/s per layer
- **Processing:** Display server handles layer compositing

## Frame Rate Control

The `-d` / `--delay` flag controls frame rate by adding a delay between frames.

```bash
# No delay (as fast as possible)
python -m flaschen_taschen.demos.plasma -d 0

# 50ms delay = ~20 FPS
python -m flaschen_taschen.demos.plasma -d 50

# 100ms delay = ~10 FPS
python -m flaschen_taschen.demos.plasma -d 100
```

**Why add delay?**
- Reduces CPU usage (lets the system breathe)
- Gives network time to transmit frames
- Makes animations more readable at higher refresh rates

## Geometry & Performance

The number of pixels affects performance:

| Geometry | Pixels | Typical Use |
|----------|--------|------------|
| 20x20 | 400 | Small window, fast |
| 45x35 | 1,575 | Default, balanced |
| 45x70 | 3,150 | Large window, slower |

**Recommendation:** Use default 45x35 unless you have a specific reason to change it.

## Python Optimization

### Pure Python vs NumPy

Some demos (plasma, matrix) have optional numpy acceleration:

```python
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
```

Install numpy for faster math:
```bash
pip install flaschen-taschen-py[numpy]
```

Expected speedups:
- **Plasma:** 2-3x faster with numpy
- **Matrix:** minimal difference (doesn't use heavy math)
- **Fractal:** 5-10x faster with numpy (Mandelbrot computation)

### Algorithm Efficiency

**Good practices:**
- Cache pre-computed values (sine lookup tables, palettes)
- Avoid recalculating each frame what was computed in setup()
- Use integer arithmetic instead of floats
- Minimize nested loops

**Example: Pre-compute a sine table**
```python
class SineDemo(Demo):
    def setup(self):
        super().setup()
        # Pre-compute once
        self.sine_table = [math.sin(i * 2 * math.pi / 256) for i in range(256)]

    def draw(self):
        # Look up instead of computing
        val = self.sine_table[self.frame % 256]
```

## Canvas Operations

### Batch Operations

Minimize individual pixel sets:

```python
# Slow: 1,575 calls to set_pixel
for y in range(self.canvas.height):
    for x in range(self.canvas.width):
        self.canvas.set_pixel(x, y, color)

# Better: One fill_rect
self.canvas.fill(color)

# Better: Use filled shapes
self.canvas.draw_circle(cx, cy, radius, color, filled=True)
```

### Clear Strategy

```python
# Good: Clear once per frame
self.canvas.clear()
# Draw...

# Avoid: Multiple clears per frame
self.canvas.clear()
# Draw...
self.canvas.clear()  # unnecessary!
# Draw more...
```

## Network Performance

### Auto-Send vs Manual

The `Canvas` automatically sends frames if `auto_send=True`:

```python
# Automatic (good for most cases)
canvas = Canvas(auto_send=True)
canvas.set_pixel(...)
canvas.send()  # Sends automatically

# Manual (if you want fine-grained control)
canvas = Canvas(auto_send=False)
canvas.set_pixel(...)
canvas.send(force=True)  # Send only when you want
```

### Layered Display

Use layers efficiently:

```python
# Layer 0 = rendered on top
# Layer 15 = rendered on bottom

# Put static content on higher layers, update lower layers
canvas_layer0 = layered.get_layer_canvas(0)  # Updated each frame
canvas_layer1 = layered.get_layer_canvas(1)  # Static background
```

## Profiling Your Demo

### Measure FPS

The Demo class provides FPS info:

```python
def draw(self):
    print(f"FPS: {self.fps:.1f}")  # Print each frame
```

### Time Critical Sections

Use Python's `timeit` for profiling:

```python
import timeit

def your_algorithm():
    # Your code here
    pass

duration = timeit.timeit(your_algorithm, number=1000)
print(f"1000 iterations: {duration:.3f}s ({duration/1000*1000:.1f}ms each)")
```

## Typical Performance

On a modern machine with default 45x35 geometry:

| Demo | FPS (no delay) | FPS (50ms delay) |
|------|---------|---------|
| Simple pixel ops | 30+ FPS | 20 FPS |
| Plasma | 25+ FPS | ~20 FPS |
| Matrix | 20+ FPS | ~20 FPS |
| Fractal | 10+ FPS | ~10 FPS |
| Game of Life | 15+ FPS | ~15 FPS |

**Note:** Network latency is usually the limiting factor, not Python performance.

## Network Bandwidth

Each frame is a PPM image sent over UDP:

```
Frame size = width * height * 3 bytes (RGB) + PPM header
45x35 = ~4.7 KB per frame
At 30 FPS = ~140 KB/s
```

This fits comfortably in typical WiFi bandwidth.

## Troubleshooting Slow Performance

**Problem:** Demo runs slowly (choppy)

**Solutions:**
1. Add frame delay: `-d 50`
2. Reduce geometry: `-g 20x20`
3. Switch to a simpler demo
4. Check network latency: `ping display.local`
5. Install numpy: `pip install numpy`

**Problem:** CPU usage is high

**Solutions:**
1. Add frame delay: `-d 100` (even more delay)
2. Use a demo with fewer pixels being written
3. Simplify your algorithm
4. Consider running on a faster machine

**Problem:** Display shows lag/stutter

**Solutions:**
1. Check network: `ping display.local`
2. Move closer to WiFi router
3. Reduce frame rate: `-d 100`
4. Check other network activity

## Best Practices Summary

1. **Use default geometry** (45x35) unless you have a reason to change
2. **Add frame delay** (`-d 50` or `-d 100`) unless you need high FPS
3. **Cache pre-computed values** (lookup tables, palettes)
4. **Minimize per-frame calculations** — move them to `setup()`
5. **Use built-in shapes** (`fill_rect`, `draw_circle`) instead of pixel loops
6. **Profile before optimizing** — measure, then optimize
7. **Consider numpy** for math-heavy demos
8. **One `send()` per frame** — the Demo framework handles this

## Further Reading

- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed)
- [NumPy Performance](https://numpy.org/devdocs/user/basics.broadcasting.html)
- FlaschenTaschen C++ reference implementation (for algorithms)
