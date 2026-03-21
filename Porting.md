
Original C++ code can be found below for the server, clients and demos.

~/Developer/FT/flaschen-taschen
~/Developer/FT/ft-demos

The Swift port is at this path.

~#~/Developer/FlaschenTaschen/ft-swift

See the README.md for the details.

For this we will create a Python port which is equivalent to the Swift port which has organized the server, client and demos together along with libaries to gather reusable features to make it easier to create new code to drive FT displays.

## Demo Source Code Mapping

Quick reference for finding demo implementations across C++, Swift, and Python versions.

**Swift demos are organized in two places:**
1. **Entry Point** (`ft-swift/Sources/[demo]/[Demo].swift`) — Contains CLI argument parsing and main loop
2. **Implementation** (`ft-swift/Sources/FlaschenTaschenDemoKit/Demos/[Demo]Demo.swift`) — Core algorithm and drawing logic

| Demo | C++ | Swift Entry Point | Swift Implementation | Python |
|------|-----|------|------|--------|
| Black | `ft-demos/src/black.cc` | `ft-swift/Sources/black/Black.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/BlackDemo.swift` | `demos/black.py` |
| Blur | `ft-demos/src/blur.cc` | `ft-swift/Sources/blur/Blur.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/BlurDemo.swift` | `demos/blur.py` |
| Depth | — | `ft-swift/Sources/depth/Depth.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/DepthDemo.swift` | — |
| Firefly | — | `ft-swift/Sources/firefly/Firefly.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/FireflyDemo.swift` | `demos/firefly.py` |
| Fractal | `ft-demos/src/fractal.cc` | `ft-swift/Sources/fractal/Fractal.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/FractalDemo.swift` | — |
| Hack | `ft-demos/src/hack.cc` | `ft-swift/Sources/hack/Hack.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/HackDemo.swift` | — |
| Life | `ft-demos/src/life.cc` | `ft-swift/Sources/life/Life.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/LifeDemo.swift` | — |
| Lines | `ft-demos/src/lines.cc` | `ft-swift/Sources/lines/Lines.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/LinesDemo.swift` | — |
| Matrix | `ft-demos/src/matrix.cc` | `ft-swift/Sources/matrix/Matrix.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/MatrixDemo.swift` | `demos/matrix.py` |
| Maze | `ft-demos/src/maze.cc` | `ft-swift/Sources/maze/Maze.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/MazeDemo.swift` | — |
| NB Logo | `ft-demos/src/nb-logo.cc` | `ft-swift/Sources/nb-logo/NbLogo.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/NbLogoDemo.swift` | — |
| Plasma | `ft-demos/src/plasma.cc` | `ft-swift/Sources/plasma/Plasma.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/PlasmaDemo.swift` | `demos/plasma.py` |
| Quilt | `ft-demos/src/quilt.cc` | `ft-swift/Sources/quilt/Quilt.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/QuiltDemo.swift` | `demos/quilt.py` |
| Random Dots | `ft-demos/src/random-dots.cc` | `ft-swift/Sources/random-dots/RandomDots.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/RandomDotsDemo.swift` | — |
| SF Logo | — | `ft-swift/Sources/sf-logo/SfLogo.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/SfLogoDemo.swift` | — |
| Sierpinski | `ft-demos/src/sierpinski.cc` | `ft-swift/Sources/sierpinski/Sierpinski.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/SierpinskiDemo.swift` | — |
| Simple Animation | `ft-demos/src/simple-animation.cc` | `ft-swift/Sources/simple-animation/SimpleAnimation.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/SimpleAnimationDemo.swift` | `demos/simple_animation.py` |
| Simple Example | `ft-demos/src/simple-example.cc` | `ft-swift/Sources/simple-example/SimpleExample.swift` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/SimpleExampleDemo.swift` | `demos/simple_example.py` |

### How to Port a Demo

1. **Find the Swift reference**: Use the table above to locate both files:
   - **Entry Point** (`Sources/[demo]/[Demo].swift`) — Shows CLI argument parsing, StandardOptions usage, and main execution loop
   - **Implementation** (`Sources/FlaschenTaschenDemoKit/Demos/[Demo]Demo.swift`) — Contains the core algorithm and drawing logic

2. **Read the Entry Point first**: Understand how the demo:
   - Parses command-line arguments
   - Creates StandardOptions
   - Sets up the demo instance
   - Runs the main update/draw loop
   - Handles timing and timeout

3. **Read the Implementation second**: Understand the algorithm:
   - What state the demo maintains
   - How `update()` modifies state
   - How `draw()` renders to the canvas
   - Any palette or color logic

4. **Check the C++ original** (if available): For additional algorithmic context

5. **Implement in Python**: Match the Swift version's behavior exactly, including:
   - StandardOptions argument parsing
   - Lifecycle (setup, update, draw, cleanup)
   - Algorithm logic from the Demo class
   - Frame rate and timing behavior

6. **Test thoroughly**: Run the demo and compare visual output with Swift version
