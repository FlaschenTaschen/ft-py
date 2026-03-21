# FlaschenTaschen Python Port - Implementation Plan

## Overview
Create a unified Python package (`flaschen-taschen-py`) that mirrors the Swift implementation. The package will include a core client library, content generators, 15+ interactive demos, and a debugger—all using Python best practices and packaging standards.

## Execution Strategy & Key Decisions

### Progress Tracking Between Context Clears
- **PROGRESS.md** file maintains status of completed phases and current work
- At end of each phase:
  - Mark phase as `[COMPLETE]` with date/timestamp
  - Document what was implemented
  - List any blockers or incomplete items
  - Note file structure and key decisions made
- When context is cleared, PROGRESS.md is read to resume at the correct phase
- User commits code changes to git; I never commit

### Implementation Approach - CRITICAL DISCIPLINE REQUIRED
- **READ SWIFT REFERENCE FIRST**: Before implementing ANY demo or feature:
  1. Locate the corresponding `.swift` file in `~/Developer/FlaschenTaschen/ft-demos/Sources/FlaschenTaschenDemoKit/Demos/`
  2. Read it completely to understand the exact algorithm, data structures, and behavior
  3. Compare Python implementation against the Swift reference line-by-line
  4. **DO NOT GUESS** at algorithms or behavior - follow the reference exactly
  5. Document any differences between Swift and Python in comments if truly necessary
- **Phased Development**: Implement and test one phase at a time; progress tracked in PROGRESS.md for context resumption
- **Reference Code**: Use Swift port as PRIMARY and AUTHORITATIVE reference (better organized, consistent CLI); fall back to C++ code only when Swift is unclear
- **Testing**: Use existing Mac FT server app for validation; screenshots captured automatically during testing for debugging assistance
- **Git Management**: User manages ALL git commits. **I will NEVER make any git commits.** Progress tracked in PROGRESS.md between context clears.
- **Code Quality**: Include appropriate comments in code for review and ongoing development; update README.md after porting

### Dependency Decisions
- **Bitmap Fonts**: Use built-in bitmap fonts for text rendering (no Pillow dependency for text operations)
- **Numpy**: Optional performance booster; when numpy unavailable, fallback to pure Python algorithms
  - Setup documentation should encourage numpy installation for best performance
  - Demos use `try: import numpy` pattern with fallback implementations
- **Package Distribution**: This is a reusable Python package meant for distribution
  - Guidance on PyPI publishing and package structure will be provided as needed
  - Follow Python packaging best practices (setup.py, pyproject.toml, wheel distribution)

## Project Structure
```
ft-py/
├── flaschen_taschen/              # Main package
│   ├── __init__.py
│   ├── client/                    # Core library (mirrors FlaschenTaschenClientKit)
│   │   ├── __init__.py
│   │   ├── udp_client.py         # UDP communication
│   │   ├── ppm_formatter.py      # PPM binary format + FT metadata
│   │   ├── canvas.py             # Canvas/rendering abstraction
│   │   ├── color.py              # Color utilities
│   │   └── config.py             # Configuration (geometry, frame rates, etc.)
│   ├── generators/                # Content generators
│   │   ├── __init__.py
│   │   ├── text.py               # send-text functionality
│   │   ├── image.py              # send-image functionality
│   │   └── video.py              # send-video functionality
│   └── utils/
│       ├── __init__.py
│       ├── math.py               # Math utilities for demos
│       └── palette.py            # Color palettes
├── demos/                         # Interactive demo targets
│   ├── simple_example.py
│   ├── simple_animation.py
│   ├── plasma.py
│   ├── matrix.py
│   ├── blur.py
│   ├── quilt.py
│   ├── firefly.py
│   ├── depth.py
│   ├── random_dots.py
│   ├── life.py
│   ├── fractal.py
│   ├── sierpinski.py
│   ├── maze.py
│   ├── lines.py
│   ├── hack.py
│   ├── words.py
│   ├── nb_logo.py
│   ├── sf_logo.py
│   ├── midi.py
│   ├── kbd2midi.py
│   └── black.py
├── bin/                           # Executable scripts
│   ├── send-text
│   ├── send-image
│   ├── send-video
│   └── ft-debugger
├── tests/
│   ├── test_client.py
│   ├── test_ppm_formatter.py
│   ├── test_canvas.py
│   ├── test_generators/
│   │   ├── test_text.py
│   │   ├── test_image.py
│   │   └── test_video.py
│   └── test_demos/               # Basic demo validation tests
├── pyproject.toml                 # Modern Python packaging
├── setup.py                       # Fallback for compatibility
├── setup.cfg                      # Installation config
├── MANIFEST.in                    # Include non-Python files
├── requirements.txt               # Runtime dependencies
├── requirements-dev.txt           # Development dependencies
├── Makefile                       # Build targets (analogous to build.sh)
├── README.md                      # Project documentation
└── LICENSE                        # MIT License

```

## Standard Options (Used by All Demos and Tools)

All demos, generators, and tools use a unified `StandardOptions` class for consistent CLI behavior:

```python
from flaschen_taschen.standard_options import StandardOptions

std_opts = StandardOptions(sys.argv[1:])

# Available attributes:
std_opts.hostname      # Display hostname (default: localhost)
std_opts.width         # Display width (from geometry)
std_opts.height        # Display height (from geometry)
std_opts.xoff          # X offset (from geometry)
std_opts.yoff          # Y offset (from geometry)
std_opts.layer         # Layer 0-15 (default: 0)
std_opts.delay         # Frame delay in milliseconds (default: 0)
std_opts.timeout       # Timeout in seconds (default: 10)
std_opts.non_standard_args  # Remaining args for tool-specific parsing
```

**Standard Arguments** (all demos support these):
```
-h, --host HOST           Display hostname/IP (default: localhost)
-g, --geometry WxH[+X+Y]  Display geometry (default: 45x35)
-l, --layer LAYER         Layer 0-15 (default: 0)
-d, --delay MS            Frame delay in milliseconds (default: 0)
-t, --timeout SECS        Timeout in seconds (default: 10)
```

**Tool-Specific Arguments**: Each tool adds additional args after parsing standard options.

---

## Implementation Phases

### Phase 1: Core Library Foundation
**Deliverable**: `flaschen_taschen.client` module with basic UDP communication

1. **UDP Client** (`client/udp_client.py`)
   - Implement UDP socket communication on port 1337
   - Handle connection to display by hostname/IP
   - Support default localhost connection
   - Connection timeout and error handling

2. **PPM Formatter** (`client/ppm_formatter.py`)
   - Parse/generate PPM binary (P6) format
   - Implement FT metadata extensions (#FT: x y z)
   - Support multi-layer rendering with layer offsets
   - Automatic byte encoding/decoding

3. **Canvas/Rendering** (`client/canvas.py`)
   - Abstract pixel-setting interface
   - Support configurable geometry (width, height, x_offset, y_offset)
   - Layer management (0-15 layer range)
   - Multi-layer compositing with transparency
   - Frame rate control and buffering
   - Auto-send and flush mechanisms

4. **Color Support** (`client/color.py`)
   - RGB color class
   - Named color constants
   - Color palette utilities
   - Hex/string parsing for CLI tools

5. **Configuration** (`client/config.py`)
   - Geometry configuration
   - Default settings (1337 port, localhost, 45x35 default)
   - Frame delay and timeout settings
   - Display server detection/validation

**Testing**: Unit tests for UDP communication, PPM encoding/decoding, canvas operations

---

### Phase 2: Content Generators
**Deliverable**: `send-text`, `send-image`, `send-video` CLI tools

1. **Text Generator** (`generators/text.py` + `bin/send-text`)
   - Render text with built-in bitmap fonts (5x5 monospace)
   - Scrolling text support
   - Static text option
   - Color palette selection
   - Font size/style options via bitmap upscaling (2x, 3x, etc.)
   - **No external font dependencies**: Pure Python bitmap rendering

2. **Image Generator** (`generators/image.py` + `bin/send-image`)
   - Load image files (PNG, JPEG, BMP, etc. via Pillow)
   - Resize/scale to display geometry
   - Dithering for color reduction
   - Layer offset support
   - **RPi Optimization**: Stream large images in chunks; optional Pillow dependency with pure Python fallback

3. **Video Generator** (`generators/video.py` + `bin/send-video`)
   - Frame extraction from video files (ffmpeg via subprocess; no opencv-python)
   - Real-time streaming
   - Frame rate control
   - Scale to geometry
   - **RPi Optimization**: Encode/decode via system ffmpeg; frame buffering to manage memory

**CLI Argument Parsing**:
- Common args: `-g <W>x<H>[+<X>+<Y>]` (geometry), `-h <host>` (hostname), `-l <layer>` (layer 0-15), `-d <delay>` (ms), `-t <timeout>` (seconds)
- Use argparse for argument handling

**Testing**: Integration tests with mock display server

---

### Phase 3: Debugger
**Deliverable**: `ft-debugger` interactive tool

1. **Color Palette Selection**
   - Support 8-16 color palettes
   - HSV/RGB palette generation

2. **Display Modes**
   - Draw edges (outline) in selected color
   - Fill entire display with color
   - Interactive color/palette switching

3. **Network Validation**
   - Ping/test display connection
   - Display geometry detection

**Testing**: Manual testing with display connection

---

### Phase 4: Interactive Demos (Batch 1 - Simple Examples)
**Deliverable**: Core demo framework + 7 initial demos

1. **Demo Framework** (`demos/__init__.py`)
   - Base `Demo` class with lifecycle methods:
     - `__init__(std_opts)` — receive StandardOptions with standard args already parsed
     - `setup()` — initialize canvas and resources
     - `update()` — compute frame logic
     - `draw()` — render to canvas
     - `send()` — transmit frame
     - `cleanup()` — release resources
   - Uses `StandardOptions` for consistent CLI arg handling (see above)
   - Entry point decorator for CLI discovery
   - **Performance profiling hooks** for benchmarking on Raspberry Pi
   - **Frame rate control**: Adaptive delay to maintain target FPS without overloading RPi CPU

2. **Simple Examples** (Essential for RPi)
   - `simple_example.py` — Colored rectangles (pure Python, minimal load)
   - `simple_animation.py` — Animated shapes (pure Python)
   - `black.py` — Clear display (minimal)

3. **Generative Graphics (Phase 4)** (RPi performance-optimized)
   - `plasma.py` — Smooth plasma with color cycling (pure Python baseline; numpy acceleration available)
   - `matrix.py` — Matrix-style rain (pure Python, simple algorithm)
   - `blur.py` — Gaussian blur (pure Python convolution; numpy significantly faster for large kernels)
   - `quilt.py` — Procedural quilt pattern (pure Python, seed-based generation)
   - `firefly.py` — Wandering particles with trails (pure Python, simple physics)

**Testing**: Visual inspection, performance profiling on Raspberry Pi (ensure 30 FPS minimum)

---

### Phase 5: Interactive Demos (Batch 2 - Advanced)
**Deliverable**: 8+ additional demos (with RPi scaling)

1. **Mathematical & Algorithmic** (Pure Python, CPU-efficient)
   - `life.py` — Conway's Game of Life (essential; optimized with pre-computed neighborhoods)
   - `fractal.py` — Julia set + Mandelbrot (optional; CPU-intensive; provide low-resolution mode for RPi)
   - `sierpinski.py` — Sierpinski triangle (essential; seed-based generation)
   - `maze.py` — Procedural maze generator (essential; simple recursive algorithm)
   - `lines.py` — Algorithmic line patterns (essential; Bresenham's line algorithm)

2. **Visual Effects** (Pure Python, performance-tuned)
   - `depth.py` — 3D depth map visualization (optional; pure Python 3D projection)
   - `random_dots.py` — Bouncing particle system (essential; simple physics, no numpy required)

3. **Text & Logos** (Requires Pillow for font rendering)
   - `hack.py` — Rotating vector font with blur (optional; computationally expensive; Pillow required)
   - `words.py` — Streaming text (optional; Pillow for font rendering; fallback to bitmap fonts)
   - `nb_logo.py` — Noisebridge logo animation (optional; SVG to bitmap; Pillow recommended)
   - `sf_logo.py` — Sequoia Fabrica logo animation (optional; SVG to bitmap; Pillow recommended)

4. **Interactive** (Mido-based, cross-platform)
   - `midi.py` — MIDI keyboard input visualization (optional; requires mido + MIDI hardware)
   - `kbd2midi.py` — Computer keyboard to MIDI (optional; requires mido + portaudio)

**RPi Scaling Strategy**:
- **Tier 1 (Essential, always test)**: life, sierpinski, maze, lines, random_dots, simple examples, plasma, matrix
- **Tier 2 (Recommended, test on capable systems)**: quilt, firefly, blur, words
- **Tier 3 (Optional, heavy, skip on RPi)**: fractal, hack, depth, nb_logo, sf_logo, midi

**Testing**: Demo validation suite, parameter coverage tests, Raspberry Pi performance profiling

---

### Phase 6: Packaging & Distribution
**Deliverable**: PyPI-ready package

1. **Setup Infrastructure**
   - `pyproject.toml` with build backend (setuptools/hatch)
   - `setup.py` for compatibility
   - `setup.cfg` with metadata
   - `MANIFEST.in` for non-Python assets

2. **Dependencies**
   - Core: `socket` (stdlib), minimal external deps
   - Optional: `pillow` (images), `opencv-python` or `ffmpeg-python` (video), `pygame` or `mido` (MIDI)
   - Dev: `pytest`, `pytest-cov`, `black`, `isort`, `mypy`

3. **Entrypoints**
   - CLI commands in `bin/` as console_scripts
   - Demo discovery as dynamic entry points

4. **Build System**
   - `Makefile` targets: `make install`, `make test`, `make lint`, `make build`, `make clean`
   - GitHub Actions CI/CD (optional)

---

### Phase 7: Documentation & Testing
**Deliverable**: Complete documentation and test suite

1. **Documentation**
   - Comprehensive README.md (mirror Swift README structure)
   - API reference (auto-generated from docstrings)
   - Architecture diagram (copy from Swift)
   - Quick start guide with examples
   - Porting notes (what changed from C++/Swift)

2. **Test Suite**
   - Unit tests for core library (70%+ coverage)
   - Integration tests for generators
   - Demo validation tests
   - Mock UDP server for testing without real hardware

3. **Examples**
   - Minimal `main.py` equivalent to Swift example
   - Common usage patterns

---

## Key Dependencies

### Platform Requirements
- **Python 3.8+** (3.8 chosen for broad Raspberry Pi compatibility)
- **No platform-specific system libraries** — all dependencies must build on macOS, Linux (x86/ARM), and Raspberry Pi
- Cross-platform testing required (macOS, Linux x86_64, Linux ARM32/ARM64)

### Core Runtime
- **socket** (stdlib) — UDP communication
- **struct** (stdlib) — Binary packing for PPM format
- **threading** (stdlib) — Async layer timeout management
- **time** (stdlib) — Timing and frame rate control

### Optional (Conditional Imports - Cross-Platform Only)
- **Pillow** (`python3-pil` on Raspberry Pi) — Image loading only (send-image)
  - Pure Python + cross-platform C extensions
  - Used only for image file loading; text rendering uses built-in bitmap fonts
  - Optional: if Pillow unavailable, send-image gracefully degrades
- **ffmpeg-python** — Video decoding via subprocess (send-video)
  - Requires `ffmpeg` system package (available on all platforms)
  - More portable than opencv-python (no native compilation needed on Raspberry Pi)
- **numpy** (optional, for performance) — Numerical operations in demos
  - Significantly speeds up mathematical operations (plasma, fractals, blur)
  - If unavailable, demos fall back to pure Python implementations (slower but functional)
  - **Recommended in setup**: Users encouraged to install for better performance, especially on multi-core systems
  - Pattern: `try: import numpy as np; except ImportError: np = None` then conditional logic
- **mido** (`python3-mido` on Raspberry Pi) — MIDI support (midi, kbd2midi)
  - Pure Python, cross-platform
  - Requires `portaudio-dev` on Linux/Raspberry Pi for sound I/O

### NOT Included (Platform-Specific, Avoided)
- ~~opencv-python~~ — Heavy native compilation, poor Raspberry Pi support; use ffmpeg-python instead
- ~~pygame~~ — GUI features not needed; use mido for MIDI only
- ~~scipy~~ — Heavy numeric library; use numpy if needed, pure Python math where possible
- ~~AppKit, Foundation~~ — macOS-specific; avoid all Apple frameworks

### Development
- **pytest** — Test framework (cross-platform)
- **pytest-cov** — Coverage reporting
- **black** — Code formatting
- **isort** — Import sorting
- **flake8** — Linting (lightweight alternative to mypy for broad compatibility)

### System Packages (for optional features)
```bash
# Debian/Raspberry Pi
sudo apt-get install python3-pil python3-mido ffmpeg portaudio-dev

# macOS (Homebrew)
brew install ffmpeg portaudio

# Fedora/RHEL
sudo dnf install python3-pillow ffmpeg portaudio-devel
```

---

## Design Decisions

1. **Modularity**: Each demo is a standalone script using the core library, not a shared monolithic codebase
2. **CLI Consistency**: All tools share common argument patterns (geometry, host, layer, delay, timeout)
3. **Layer Support**: Maintain multi-layer rendering with timeout management (from Swift)
4. **Optional Dependencies**: Keep core library lightweight; optional features loaded only when needed
5. **Entry Points**: Use setuptools console_scripts for seamless CLI integration
6. **Naming**: Use Python conventions (snake_case for modules/functions, CamelCase for classes)
7. **Cross-Platform Compatibility**: No Apple-specific libraries or frameworks; all dependencies must build/run on Raspberry Pi
8. **Pure Python Fallbacks**: Demos use pure Python algorithms where performance allows; numpy/heavy libraries optional only
9. **Numpy Conditional Pattern**: All demos use `try: import numpy except ImportError` pattern with dual implementations (numpy-accelerated + pure Python)
10. **Code Comments**: Include comments explaining non-obvious logic for code review and maintenance
11. **Bitmap Fonts**: Text rendering uses built-in 5x5 bitmap fonts; no Pillow font dependency

---

## Code Quality & Documentation Strategy

### Comments & Code Review
- Include comments for non-obvious algorithms, especially when ported from C++ or Swift
- Document why certain design choices were made (e.g., "prefer list over array for sparse data")
- Comment tricky edge cases, performance optimizations, and platform-specific workarounds
- Aim for code that supports ongoing development and review

### Testing & Validation
- **Automated**: Unit tests for core library, mock server tests for demos
- **Visual**: Use Mac app to capture screenshots during demo execution for validation
- **Phase Completion**: Commit after each phase; context is cleared before next phase
- **Performance**: Profile on Raspberry Pi to ensure frame rate targets

### Documentation Updates
- **After Phase 7** (or incrementally): Update main README.md to document:
  - Setup instructions including numpy recommendation
  - Installation on macOS, Linux, Raspberry Pi
  - Quick start examples (mirrors Swift README structure)
  - API reference for the client library
  - Performance tuning guide
  - Contributing guide for new demos

### Package Distribution Guidance
- Will provide step-by-step guidance on:
  - Creating proper `pyproject.toml` with build metadata
  - Publishing to PyPI (test PyPI first, then production)
  - Wheel generation and distribution
  - Versioning strategy (semantic versioning)
  - Dependency specification (core vs. optional)

---

## Platform-Specific Considerations

### macOS
- Full support for all features
- Install dependencies: `brew install ffmpeg portaudio`
- Python 3.8+ via Homebrew or python.org
- All optional packages (Pillow, numpy, mido) available via pip with pre-built wheels

### Linux (x86_64)
- Full support; all features tested on Ubuntu 20.04+, Fedora, Debian
- System packages: `sudo apt-get install python3-pil ffmpeg portaudio-dev` (Debian/Ubuntu)
- Python 3.8+ available in all major distributions

### Raspberry Pi (ARMv7/ARMv8)
- **Target**: Raspberry Pi 3B+ and newer (minimum 1GB RAM)
- **OS**: Raspberry Pi OS (Debian-based)
- **Python**: System python3 (3.9+) or pyenv for newer versions
- **Key Constraints**:
  - Limited RAM: avoid memory-heavy dependencies (e.g., opencv-python)
  - Limited CPU: demos must be CPU-efficient; provide frame rate control and lightweight fallbacks
  - No pre-built wheels for many packages: compile time considerations
- **Optimization Strategy**:
  - Use ffmpeg-python (subprocess-based, no native compilation)
  - Pillow: lightweight image operations, avoid heavy processing
  - Demos: pure Python for algorithms, optional numpy for SIMD where needed
  - Performance profiling: ensure 30 FPS achievable on RPi 3B+
- **Install on Raspberry Pi**:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-pip python3-pil python3-mido ffmpeg portaudio-dev
  pip3 install flaschen-taschen-py
  ```

### Reference: C++ Approach
The original C++ implementation (`~/Developer/FT/flaschen-taschen`) demonstrates key cross-platform patterns:
- Uses standard POSIX/BSD sockets for UDP (works everywhere)
- Minimal external dependencies; graphics handled with PPM format (no graphics library requirement)
- Demos written in portable C++; no platform-specific graphics/input libraries
- Build system (Make/CMake) handles platform differences transparently
- Python port follows same philosophy: lightweight, portable, minimal dependencies

---

## Testing Strategy

### Platform Matrix
```
macOS + python3.8   ✓ Full test suite
macOS + python3.11  ✓ Full test suite
Linux x86 + py3.8   ✓ Full test suite
Linux x86 + py3.11  ✓ Full test suite
Linux ARM + py3.9   ✓ Lightweight test suite (subset)
Raspberry Pi + py3.9 ✓ Core library + essential demos only
```

### CI/CD Configuration
- GitHub Actions: Test macOS (latest) + Ubuntu 20.04/22.04 (x86_64)
- Manual/periodic: Test on actual Raspberry Pi hardware or QEMU ARM emulation
- Coverage target: 70%+ for core library (consistent across platforms)

### Demo Validation
- **Essential demos** (always test): simple_example, simple_animation, black, plasma, life
- **Optional demos** (test on capable systems): hack, fractal, video processing (heavy deps)
- **Performance gates**: All essential demos must achieve 30 FPS on Raspberry Pi 3B+ at 45x35 resolution

### Dependency Testing
- Test each optional dependency in isolation (feature gates)
- Verify graceful degradation when optional packages missing
- Mock external tools (ffmpeg) in unit tests; integration tests use real tools

---

## Success Criteria

### Core Functionality
- [ ] Core UDP client library passing unit tests
- [ ] PPM format encoder/decoder validated
- [ ] Canvas abstraction supports multi-layer rendering
- [ ] 3 content generators (send-text, send-image, send-video) working
- [ ] ft-debugger interactive tool functional
- [ ] 15+ demos ported and validated
- [ ] PyPI package publishable with metadata
- [ ] README matches Swift port structure
- [ ] 70%+ test coverage for core library
- [ ] All demos run with `-h localhost` without errors

### Cross-Platform Validation
- [ ] All code runs on macOS 11+, Linux (x86_64), and Raspberry Pi OS
- [ ] No platform-specific imports or system calls (except where documented)
- [ ] Optional dependencies gracefully skip if unavailable (feature gates)
- [ ] Tested on Python 3.8+ (minimum), 3.11+ (recommended)
- [ ] Essential demos achieve 30 FPS on Raspberry Pi 3B+ (45x35 resolution)
- [ ] Installation via pip works on all platforms without manual compilation
- [ ] System package installation documented for macOS, Ubuntu, Fedora, Raspberry Pi OS
- [ ] CI/CD validates macOS + Ubuntu; manual RPi testing on real hardware or emulation

---

## Build & Development on Each Platform

### macOS Development
```bash
# Install Python 3.8+
brew install python@3.11 ffmpeg portaudio

# Create venv and install
python3.11 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
make test

# Build package
make build
```

### Linux (Ubuntu/Debian) Development
```bash
# Install Python 3.8+
sudo apt-get install python3.11 python3.11-venv ffmpeg portaudio-dev

# Create venv and install
python3.11 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
make test
```

### Raspberry Pi Development
```bash
# On Raspberry Pi OS (bullseye or bookworm)
sudo apt-get update
sudo apt-get install python3-pip python3-venv python3-pil ffmpeg portaudio-dev

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install (skip heavy optional deps)
pip install flaschen-taschen-py
# Or for development:
pip install -e ".[dev-lite]"  # Excludes numpy, heavy optional deps

# Test essential demos
python demos/simple_example.py -g 45x35

# Profile performance
time python demos/plasma.py -g 45x35 -t 5  # 5-second run, check timing
```

### Profiling on Raspberry Pi
- Use `cProfile` to identify bottlenecks: `python -m cProfile -s cumtime demos/plasma.py -t 5`
- Monitor frame rate: add timing prints to Demo.update()/send()
- Monitor memory: `top` or `ps aux` during demo execution
- CPU scaling: may need to adjust OS governor or cool Pi if throttling occurs

---

## Reference: Learning from C++ Original

The original Flaschen Taschen C++ implementation (`~/Developer/FT/flaschen-taschen`) and demos (`~/Developer/FT/ft-demos`) provide important reference patterns:

1. **Socket Code**: Use standard POSIX sockets for UDP (not platform-specific APIs)
2. **Format**: PPM binary format requires no external graphics libraries
3. **Minimal Dependencies**: Demos link only libm (math) and platform pthread; no graphics/UI frameworks
4. **Algorithm Porting**: Many demos in ft-demos can be directly ported to Python with minimal changes
5. **Performance**: C++ demos include timing loops and frame rate control—Python should follow same patterns
6. **Build System**: Simple Makefile; Python equivalent is Makefile with make targets
7. **Testing**: C++ version includes network testing harness; Python should have similar mock server

Key files to reference:
- `flaschen-taschen/api/udp-client.cc` — UDP protocol implementation
- `flaschen-taschen/api/ft-library.cc` — Client library abstraction
- `ft-demos/[demo-name].cc` — Individual demo algorithms to port

---

## Future Enhancements (Post-MVP)
- Async demo execution (asyncio)
- Web-based demo viewer (Flask/FastAPI)
- Performance benchmarking suite (automated Raspberry Pi testing)
- Conda package distribution (especially for Raspberry Pi)
- Docker image for easy demo execution (multi-arch: amd64, arm32v7, arm64v8)
- Live demo browser/playlist feature
- C extension for hot-path performance on Raspberry Pi (if benchmarking shows need)
