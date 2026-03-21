# FlaschenTaschen Test Scripts

Simple wrapper scripts for testing the Python content generators with default settings.

These scripts run directly from the project code—**no installation required**. They set `PYTHONPATH` automatically to find the local `flaschen_taschen` package.

## Usage

All scripts default to:
- **Host**: `localhost`
- **Geometry**: `45x35`

### send-text.sh

Display text on the FT display.

```bash
./scripts/send-text.sh "Hello World"
./scripts/send-text.sh --no-scroll "Static text"
./scripts/send-text.sh -s 2 "Larger text"
./scripts/send-text.sh -c ff0000 "Red text"
```

### send-image.sh

Display an image on the FT display.

```bash
./scripts/send-image.sh path/to/image.png
./scripts/send-image.sh -l 2 image.jpg  # Layer 2
```

### send-video.sh

Stream video to the FT display.

```bash
./scripts/send-video.sh path/to/video.mp4
./scripts/send-video.sh -fps 24 video.mp4
./scripts/send-video.sh -duration 10 video.mp4  # 10 seconds
```

## Override Defaults

Pass any additional arguments to override defaults:

```bash
./scripts/send-text.sh --host 192.168.1.100 -g 60x40 "Custom host and size"
./scripts/send-image.sh -g 45x35+5+5 image.png  # With offset
```

## Interactive Demos (Phase 4)

Phase 4 adds 8 interactive demos. Run them with the `demos.sh` master script:

### Master Demo Script

```bash
./scripts/demos.sh [demo_name] [options]
./scripts/demos.sh --help          # Show help
```

### Available Demos

```bash
./scripts/demos.sh simple_example     # Static colored rectangles
./scripts/demos.sh simple_animation   # Animated moving circles
./scripts/demos.sh black              # Clear display
./scripts/demos.sh plasma             # Smooth plasma effect
./scripts/demos.sh matrix             # Matrix-style falling characters
./scripts/demos.sh blur [type]        # Blur with shapes (bolt/boxes/circles/target/fire/all)
./scripts/demos.sh quilt              # Procedural quilt pattern
./scripts/demos.sh firefly            # Wandering particles with trails
```

### Individual Demo Scripts

Each demo also has its own run script:

```bash
./scripts/run_plasma.sh -g 45x35 -t 5
./scripts/run_matrix.sh -h display.local
./scripts/run_firefly.sh -d 50 -t 30
```

### Standard Demo Options

All demos support:
- `-h, --host HOST` — Display hostname (default: localhost)
- `-g, --geometry WxH[+X+Y]` — Display geometry (default: 45x35)
- `-l, --layer LAYER` — Layer 0-15 (default: 0)
- `-d, --delay MS` — Frame delay in milliseconds (default: 0)
- `-t, --timeout SECS` — Timeout in seconds (default: 10)

### Demo Examples

```bash
# 30-second plasma effect
./scripts/demos.sh plasma -t 30

# Matrix with custom geometry
./scripts/demos.sh matrix -g 45x35 -t 15

# Firefly on remote display
./scripts/demos.sh firefly -h display.local -t 60

# Blur with shape patterns
./scripts/demos.sh blur bolt      # Lightning bolts with blur
./scripts/demos.sh blur boxes     # Random boxes with blur
./scripts/demos.sh blur circles   # Random circles with blur
./scripts/demos.sh blur target    # Concentric circles (targets)
./scripts/demos.sh blur fire      # Vertical fire effect
./scripts/demos.sh blur all       # Cycle through all types

# Simple animation at 20 FPS for 5 seconds
./scripts/demos.sh simple_animation -d 50 -t 5
```

### Blur Demo Details

The Blur demo draws random shapes and applies repeated 3x3 blur filtering to create a blurred/fading effect:

- `bolt` — Random diagonal lines/lightning bolts
- `boxes` — Random rectangle outlines
- `circles` — Random circle outlines
- `target` — Concentric circles (target pattern)
- `fire` — Vertical line with special fire blur effect
- `all` — Automatically cycles through all types

Example:
```bash
./scripts/demos.sh blur boxes -t 30     # 30 seconds of blurred boxes
./scripts/demos.sh blur fire -d 50      # Fire effect at ~20 FPS
./scripts/demos.sh blur all -g 60x40    # Cycle all types at larger size
```
