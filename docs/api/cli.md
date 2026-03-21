# Command-Line Tools Reference

Four CLI tools provide quick access to display functionality.

## send-text

Display text on the display.

### Usage

```bash
send-text [OPTIONS] TEXT
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-g, --geometry` | 45x35 | Display geometry (WxH[+X+Y]) |
| `-h, --host` | localhost | Display hostname or IP |
| `-p, --port` | 1337 | UDP port |
| `-c, --color` | ffffff | Text color (hex, e.g., ff0000) |
| `-l, --layer` | 0 | Display layer (0-15) |
| `-d, --delay` | 0 | Frame delay in ms |
| `-t, --timeout` | 10 | Run for N seconds |
| `--scroll` | true | Scroll text (vs. static) |
| `--speed` | 1 | Scroll speed |

### Examples

```bash
# Basic
send-text "Hello World"

# To display
send-text -h display.local "Status OK"

# Custom color (red)
send-text -c ff0000 "ERROR"

# On layer 5
send-text -l 5 "Overlay"

# Custom geometry
send-text -g 20x20 "Small"

# Slow scroll
send-text --speed 0.5 "Slowly scrolling text"

# Static text (no scrolling)
send-text --scroll false "Static Message"

# Full options
send-text -g 45x35 -h display.local -c 00ff00 -d 50 -t 30 "Complex Example"
```

---

## send-image

Display an image on the display.

### Usage

```bash
send-image [OPTIONS] IMAGE_PATH
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-g, --geometry` | 45x35 | Display geometry (WxH[+X+Y]) |
| `-h, --host` | localhost | Display hostname or IP |
| `-p, --port` | 1337 | UDP port |
| `-l, --layer` | 0 | Display layer (0-15) |
| `-d, --delay` | 0 | Frame delay in ms |
| `-t, --timeout` | 10 | Run for N seconds |

### Supported Formats

PNG, JPEG, BMP, GIF, TIFF, WebP (requires Pillow)

### Examples

```bash
# Basic
send-image photo.png

# To display
send-image -h display.local photo.jpg

# Custom geometry
send-image -g 20x20 small.png

# On layer 5
send-image -l 5 overlay.png

# Long timeout
send-image -g 45x35 -h display.local -t 60 image.png

# Full options
send-image -g 45x35 -h display.local -l 2 -d 50 -t 30 photo.png
```

---

## send-video

Stream video frames to the display.

### Usage

```bash
send-video [OPTIONS] VIDEO_PATH
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-g, --geometry` | 45x35 | Display geometry (WxH[+X+Y]) |
| `-h, --host` | localhost | Display hostname or IP |
| `-p, --port` | 1337 | UDP port |
| `-l, --layer` | 0 | Display layer (0-15) |
| `-d, --delay` | 0 | Frame delay in ms |
| `-t, --timeout` | 10 | Run for N seconds |
| `-fps, --frame-rate` | 30 | Playback frame rate |
| `--duration` | None | Limit playback to N seconds |

### Requirements

- ffmpeg binary: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)

### Supported Formats

MP4, WebM, MKV, AVI, MOV, FLV, and any ffmpeg-compatible format

### Examples

```bash
# Basic
send-video video.mp4

# To display
send-video -h display.local video.mp4

# Custom frame rate
send-video -fps 24 video.mp4

# Limit to 30 seconds
send-video --duration 30 long_video.mp4

# On layer with frame delay
send-video -l 3 -d 50 video.mp4

# Full options
send-video -g 45x35 -h display.local -fps 30 -t 60 --duration 45 video.mp4
```

---

## ft-debugger

Test the display with cycling colors.

### Usage

```bash
ft-debugger [OPTIONS]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `-g, --geometry` | 45x35 | Display geometry (WxH[+X+Y]) |
| `-h, --host` | localhost | Display hostname or IP |
| `-p, --port` | 1337 | UDP port |
| `-l, --layer` | 0 | Display layer (0-15) |
| `-d, --delay` | 0 | Frame delay in ms |
| `-t, --timeout` | 5 | Run for N seconds |
| `-m, --mode` | edges | Mode: edges or fill |
| `--palette` | rainbow | Palette: rainbow or greyscale |

### Modes

- **edges** — Draw a border around the display (tests edge pixels)
- **fill** — Fill entire display (tests all pixels)

### Examples

```bash
# Test edges for 10 seconds
ft-debugger -m edges -t 10

# Test fill display
ft-debugger -m fill -t 10

# Slow mode (easy to see transitions)
ft-debugger -m fill -d 100 -t 10

# Grayscale palette
ft-debugger -m edges --palette greyscale -t 10

# Custom geometry
ft-debugger -g 20x20 -m fill -t 5

# Full options
ft-debugger -g 45x35 -h display.local -m fill -d 50 -t 30
```

---

## Common Patterns

### Testing Your Setup

```bash
# 1. Debug display connection
ft-debugger -m fill -h display.local -t 5

# 2. Send text
send-text -h display.local -t 5 "Hello"

# 3. Display image
send-image -h display.local -t 10 test.png

# 4. Run a demo
python -m flaschen_taschen.demos.plasma -h display.local -t 10
```

### Using Layers

```bash
# Background on layer 0 (red)
send-text -l 0 -c ff0000 "Background"

# Overlay on layer 1 (green)
send-text -l 1 -c 00ff00 "Overlay"

# Foreground on layer 2 (blue)
send-text -l 2 -c 0000ff "Foreground"
```

### Frame Rate Control

```bash
# Fast (no delay)
python -m flaschen_taschen.demos.plasma -d 0

# Medium (50ms delay = ~20 FPS)
python -m flaschen_taschen.demos.plasma -d 50

# Slow (100ms delay = ~10 FPS)
python -m flaschen_taschen.demos.plasma -d 100
```

---

## Troubleshooting

**"Connection refused"**
```bash
ft-debugger -h display.local -t 5
# If this fails, the display isn't reachable. Check hostname/IP.
```

**"send-text: command not found"**
```bash
pip install --force-reinstall flaschen-taschen-py
which send-text  # Verify it's installed
```

**Slow frame rate**
```bash
# Add a delay flag to reduce CPU usage
send-video -d 50 video.mp4
python -m flaschen_taschen.demos.matrix -d 50
```
