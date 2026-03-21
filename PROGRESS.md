# FlaschenTaschen Python Port - Progress Tracking

## Current Status
Phase 2 COMPLETE - Content Generators (2026-03-20)

## Completed Phases

### Phase 2: Content Generators [COMPLETE - 2026-03-20]
**Deliverable**: Text, image, and video generators with CLI tools

**What was implemented:**
1. **Bitmap Font System** (`utils/bitmap_font.py`)
   - Pure Python 5x5 monospace font
   - 95 printable ASCII characters (space to ~)
   - Scalable rendering with pixel-perfect upscaling
   - No external font dependencies

2. **Text Generator** (`generators/text.py` + `cli/send_text.py`)
   - Static text rendering at fixed position
   - Scrolling text with configurable speed
   - Font scaling (1-5x)
   - Color support via hex strings
   - CLI: `send-text -g 45x35 -c ff0000 "Hello"`

3. **Image Generator** (`generators/image.py` + `cli/send_image.py`)
   - Image loading via Pillow (PNG, JPEG, BMP, etc.)
   - Automatic resizing to display geometry
   - RGBA/RGB/grayscale support with color conversion
   - Layer offset support
   - CLI: `send-image -g 45x35 image.png`

4. **Video Generator** (`generators/video.py` + `cli/send_video.py`)
   - Frame extraction via ffmpeg subprocess
   - Real-time streaming with frame rate control
   - Duration limit support
   - Automatic frame resizing
   - CLI: `send-video -g 45x35 -fps 24 video.mp4`

5. **CLI Infrastructure**
   - Unified argument parsing for all tools
   - Common geometry format: WxH[+X+Y]
   - Layer support (0-15)
   - Host/port configuration
   - Frame delay and timeout options

6. **Test Suite** (35 new tests)
   - Bitmap font tests (7 tests)
   - Text generator tests (12 tests)
   - Image generator tests (10 tests)
   - Video generator tests (6 tests)
   - All tests passing (93 total)

**Key Decisions Made:**
- Bitmap font: Pure Python, no Pillow dependency for text
- Image/Video: Pillow required for image handling, ffmpeg via subprocess for video
- CLI tools: Use flaschen_taschen.cli package for entry points
- Scrolling: Configurable scroll speed with frame rate control

**Setup.py Updates:**
- Added console_scripts entry points for send-text, send-image, send-video
- Optional extras for image and video support (Pillow, ffmpeg-python)

**Testing Results:**
```
✓ 93 tests passed
✓ 7 bitmap font tests
✓ 12 text generator tests
✓ 10 image generator tests
✓ 6 video generator tests
✓ 58 core library tests (Phase 1)
```

### Phase 1: Core Library Foundation [COMPLETE - 2026-03-20]
**Deliverable**: `flaschen_taschen.client` module with UDP communication and rendering abstractions

**What was implemented:**
1. **UDP Client** (`client/udp_client.py`)
   - UDP socket communication on port 1337
   - DisplayConnection wrapper with rate limiting
   - Connection timeout and error handling
   - Context manager support

2. **PPM Formatter** (`client/ppm_formatter.py`)
   - P6 binary format encoding/decoding
   - FT metadata extensions (#FT: x y z)
   - Nearest-neighbor image resizing
   - Color value clamping and validation

3. **Canvas/Rendering** (`client/canvas.py`)
   - Canvas class with configurable geometry
   - Pixel manipulation (set, get, clear)
   - Primitive drawing (rectangles, lines, circles)
   - Multi-layer support (LayeredCanvas)
   - Auto-send and manual flush mechanisms
   - Frame rate control and statistics

4. **Color Support** (`client/color.py`)
   - RGB Color class with multiple creation methods
   - Named color constants (BLACK, WHITE, RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW)
   - Hex string parsing and conversion
   - ColorPalette class with wrapping support
   - HSV to RGB conversion with palette generation

5. **Configuration** (`client/config.py`)
   - Geometry configuration (width, height, x_offset, y_offset)
   - Connection settings (host, port, timeouts)
   - Frame rate control
   - Validation with detailed error messages

6. **Comprehensive Tests** (58 tests, 100% passing)
   - test_color.py (26 tests)
   - test_config.py (12 tests)
   - test_ppm_formatter.py (12 tests)
   - test_canvas.py (8 tests)

7. **Package Infrastructure**
   - pyproject.toml (modern build system)
   - setup.py (compatibility)
   - Package installable via `pip install -e .`

8. **Example Code**
   - examples/simple_test.py (demonstrates core functionality)

**Key Decisions Made:**
- Pure Python UDP with stdlib socket (no external deps)
- PPM P6 binary format (no graphics library needed)
- Separate Canvas and LayeredCanvas classes for flexibility
- HSV palette generation for demo use
- Comprehensive validation in Config class
- Draw primitives: lines (Bresenham), circles (Midpoint algorithm)

**Testing Results:**
```
✓ 58 tests passed
✓ All core library functionality verified
✓ PPM encode/decode round-trip tested
✓ Canvas drawing operations tested
✓ Color conversions tested
✓ Example runs successfully
```

## In Progress
(none - Phase 2 complete)

## Planned Phases (Not Started)
- [ ] Phase 3: Debugger (ft-debugger)
- [ ] Phase 4: Interactive Demos - Batch 1 (simple examples, generative graphics)
- [ ] Phase 5: Interactive Demos - Batch 2 (advanced algorithms, interactive)
- [ ] Phase 6: Packaging & Distribution
- [ ] Phase 7: Documentation & Testing

## Key Files Created

### Phase 1
- flaschen_taschen/__init__.py
- flaschen_taschen/client/__init__.py
- flaschen_taschen/client/config.py
- flaschen_taschen/client/color.py
- flaschen_taschen/client/udp_client.py
- flaschen_taschen/client/ppm_formatter.py
- flaschen_taschen/client/canvas.py
- tests/test_config.py
- tests/test_color.py
- tests/test_ppm_formatter.py
- tests/test_canvas.py
- pyproject.toml
- setup.py
- examples/simple_test.py

### Phase 2
- flaschen_taschen/utils/__init__.py
- flaschen_taschen/utils/bitmap_font.py
- flaschen_taschen/generators/__init__.py
- flaschen_taschen/generators/text.py
- flaschen_taschen/generators/image.py
- flaschen_taschen/generators/video.py
- flaschen_taschen/cli/__init__.py
- flaschen_taschen/cli/send_text.py
- flaschen_taschen/cli/send_image.py
- flaschen_taschen/cli/send_video.py
- tests/test_bitmap_font.py
- tests/test_generators/__init__.py
- tests/test_generators/test_text.py
- tests/test_generators/test_image.py
- tests/test_generators/test_video.py

## Context Resumption Notes
When context is cleared, read this file to determine where to resume work. Look for the current phase and incomplete items to continue from that point.

## Blockers / Issues
(none)

## Notes
- Swift code is primary reference; C++ as fallback
- Bitmap fonts for text rendering (no Pillow dependency) - Phase 2
- Numpy optional with pure Python fallback for all demos - Phase 4
- Mac app available for testing; screenshots can be captured for debugging
- All Phase 1 tests passing - ready to move to Phase 2
