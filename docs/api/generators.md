# Generators API Reference

Content generators for text, images, and video.

## TextGenerator

Render text to the display.

### Creating a TextGenerator

```python
from flaschen_taschen.generators.text import TextGenerator
from flaschen_taschen.client import Canvas, Color

canvas = Canvas(geometry="45x35", host="display.local")

gen = TextGenerator(
    canvas=canvas,
    text="Hello World",
    font_path=None,  # None = default bitmap font
    color=Color.WHITE,
    scroll=True,
    scroll_speed=1
)
```

### Methods

```python
# Static text at position
gen.render_static(x=0, y=0)

# Scrolling text
gen.render_scrolling(y=17, duration=10, frame_rate=30)

# Render (auto-selects static or scrolling)
gen.render(x=0, y=None, duration=None, frame_rate=30)
```

### Quick Send

```python
from flaschen_taschen.generators.text import send_text

send_text(
    host="display.local",
    port=1337,
    geometry="45x35",
    text="Hello",
    color=Color.RED,
    layer=0,
    delay_ms=0,
    timeout_s=10,
    scroll=True
)
```

### Examples

```python
# Static text
gen = TextGenerator(canvas, "Status: OK", color=Color.GREEN)
gen.render_static(x=5, y=5)

# Scrolling text
gen = TextGenerator(canvas, "Breaking News...", scroll=True, scroll_speed=2)
gen.render_scrolling(y=17, duration=20)

# CLI
send-text -g 45x35 -h display.local -c ff0000 "ERROR"
```

---

## ImageGenerator

Display images on the display.

### Creating an ImageGenerator

```python
from flaschen_taschen.generators.image import ImageGenerator
from flaschen_taschen.client import Canvas
from PIL import Image

canvas = Canvas(geometry="45x35", host="display.local")

# From file
gen = ImageGenerator(canvas, image_path="photo.png")

# From PIL Image object
img = Image.open("photo.png")
gen = ImageGenerator(canvas, image_data=img)
```

### Methods

```python
# Render the image
gen.render(x_offset=0, y_offset=0, duration=None)
```

### Quick Send

```python
from flaschen_taschen.generators.image import send_image

send_image(
    host="display.local",
    port=1337,
    geometry="45x35",
    image_path="photo.png",
    layer=0,
    delay_ms=0,
    timeout_s=10
)
```

### Supported Formats

- PNG, JPEG, BMP, GIF, TIFF, WebP (requires Pillow)
- Automatically resized to display geometry
- Supports RGBA, RGB, and grayscale

### Examples

```python
# Load and display image
gen = ImageGenerator(canvas, image_path="sunset.jpg")
gen.render()

# With offset
gen = ImageGenerator(canvas, image_path="logo.png")
gen.render(x_offset=10, y_offset=5)

# CLI
send-image -g 45x35 -h display.local photo.png
send-image -g 45x35 -h display.local -l 5 overlay.png
```

---

## VideoGenerator

Stream video frames to the display.

### Creating a VideoGenerator

```python
from flaschen_taschen.generators.video import VideoGenerator
from flaschen_taschen.client import Canvas

canvas = Canvas(geometry="45x35", host="display.local")

gen = VideoGenerator(
    canvas=canvas,
    video_path="video.mp4",
    frame_rate=24
)
```

### Methods

```python
# Render video
gen.render(duration=None, x_offset=0, y_offset=0)
```

### Quick Send

```python
from flaschen_taschen.generators.video import send_video

send_video(
    host="display.local",
    port=1337,
    geometry="45x35",
    video_path="video.mp4",
    layer=0,
    delay_ms=0,
    timeout_s=10,
    duration_s=30,    # Limit to 30 seconds
    frame_rate=24
)
```

### Requirements

- ffmpeg binary must be installed: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)
- Supports MP4, WebM, MKV, etc. (any ffmpeg-compatible format)

### Examples

```python
# Stream a video file
gen = VideoGenerator(canvas, "video.mp4", frame_rate=30)
gen.render(duration=60)  # 60 seconds max

# With offset and frame rate
gen = VideoGenerator(canvas, "intro.mp4", frame_rate=24)
gen.render(duration=20, x_offset=5, y_offset=5)

# CLI
send-video -g 45x35 -h display.local -fps 24 video.mp4
send-video -g 45x35 -h display.local -fps 30 -t 60 movie.mp4
```

---

## Module Summary

| Class | Purpose | Requires |
|-------|---------|----------|
| `TextGenerator` | Render text | BitmapFont (built-in) or BDFFont (custom .bdf file) |
| `ImageGenerator` | Display images | Pillow (optional dependency) |
| `VideoGenerator` | Stream video | ffmpeg binary (optional dependency) |

All generators auto-resize content to the display geometry and support layer offsets.
