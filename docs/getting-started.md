# Getting Started

## Installation

### Basic Installation
```bash
pip install flaschen-taschen-py
```

### With Optional Dependencies

For image support (PNG, JPEG, BMP, etc.):
```bash
pip install flaschen-taschen-py[image]
```

For video support (MP4, WebM, etc.):
```bash
pip install flaschen-taschen-py[video]
```

For numpy optimization (demos):
```bash
pip install flaschen-taschen-py[numpy]
```

For everything:
```bash
pip install flaschen-taschen-py[image,video,numpy]
```

## Connecting to a Display

The display server typically runs on `display.local:1337`. If you're on the same network as a FlaschenTaschen display:

```python
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")
```

**Common configuration:**
- `geometry="45x35"` — standard Noisebridge display (width x height)
- `host="display.local"` or `"192.168.1.100"` — display hostname/IP
- `port=1337` — default (usually doesn't need to change)

## Your First Script

```python
from flaschen_taschen.client import Canvas, Color
import time

# Connect to display
canvas = Canvas(geometry="45x35", host="display.local")

# Draw a red pixel
canvas.set_pixel(22, 17, Color.RED)

# Draw a rectangle
canvas.fill_rect(5, 5, 10, 10, Color.GREEN)

# Send to display
canvas.send()

# Let it display for a moment
time.sleep(2)

# Clean up
canvas.cleanup()
```

## Running a Demo

The library comes with 16 built-in demos:

```bash
# Conway's Game of Life
python -m flaschen_taschen.demos.life -t 30

# Plasma effect
python -m flaschen_taschen.demos.plasma -t 30

# Sierpinski triangle
python -m flaschen_taschen.demos.sierpinski -t 30

# Matrix rain
python -m flaschen_taschen.demos.matrix -t 30

# And more... (see Demos API for full list)
```

### Common Demo Flags

```bash
-g, --geometry WxH[+X+Y]   Display geometry (default: 45x35)
-h, --host HOSTNAME        Display hostname (default: localhost)
-l, --layer N              Layer number 0-15 (default: 0)
-d, --delay MS             Frame delay in milliseconds
-t, --timeout S            Run for N seconds then exit
```

## Command-Line Tools

### send-text — Display text on the display

```bash
send-text -g 45x35 -h display.local "Hello World"
send-text -g 45x35 -c ff0000 "Error"  # Red text
```

### send-image — Display an image

```bash
send-image -g 45x35 -h display.local photo.png
send-image -g 45x35 image.jpg
```

### send-video — Stream video

```bash
send-video -g 45x35 -h display.local -fps 24 video.mp4
```

### ft-debugger — Test the display

```bash
# Fill entire display with cycling colors for 10 seconds
ft-debugger -m fill -t 10

# Draw a border that cycles colors
ft-debugger -m edges -t 10
```

## Troubleshooting

**"Connection refused"**
- Check the display is powered on and connected to the network
- Verify the hostname or IP address
- Test with ping: `ping display.local`

**"No module named flaschen_taschen"**
- Verify installation: `pip list | grep flaschen`
- Reinstall: `pip install --force-reinstall flaschen-taschen-py`

**Slow frame rate**
- Add a delay flag: `python -m flaschen_taschen.demos.plasma -d 50`
- This gives the CPU time to breathe

**CLI tools not found**
- Reinstall the package: `pip install --force-reinstall flaschen-taschen-py`
- Verify console_scripts are installed: `which send-text`

## Next Steps

- Read the [Client API](api/client.md) for detailed class documentation
- Check the [Code Cookbook](examples/cookbook.md) for copy-paste examples
- Try [Creating Custom Demos](guides/custom-demos.md) to build your own animations
- See [Performance Tuning](guides/performance.md) for optimization tips
