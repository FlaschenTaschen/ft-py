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
