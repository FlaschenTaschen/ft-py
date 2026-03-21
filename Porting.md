
Original C++ code can be found below for the server, clients and demos.

~/Developer/FT/flaschen-taschen
~/Developer/FT/ft-demos

The Swift port is at this path.

~#~/Developer/FlaschenTaschen/ft-swift

See the README.md for the details.

For this we will create a Python port which is equivalent to the Swift port which has organized the server, client and demos together along with libaries to gather reusable features to make it easier to create new code to drive FT displays.

## Demo Source Code Mapping

Quick reference for finding demo implementations across C++, Swift, and Python versions.

| Demo | C++ | Swift | Python |
|------|-----|-------|--------|
| Black | `ft-demos/src/black.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/BlackDemo.swift` | `demos/black.py` |
| Blur | `ft-demos/src/blur.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/BlurDemo.swift` | `demos/blur.py` |
| Depth | — | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/DepthDemo.swift` | — |
| Firefly | — | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/FireflyDemo.swift` | `demos/firefly.py` |
| Fractal | `ft-demos/src/fractal.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/FractalDemo.swift` | — |
| Hack | `ft-demos/src/hack.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/HackDemo.swift` | — |
| Life | `ft-demos/src/life.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/LifeDemo.swift` | — |
| Lines | `ft-demos/src/lines.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/LinesDemo.swift` | — |
| Matrix | `ft-demos/src/matrix.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/MatrixDemo.swift` | `demos/matrix.py` |
| Maze | `ft-demos/src/maze.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/MazeDemo.swift` | — |
| NB Logo | `ft-demos/src/nb-logo.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/NbLogoDemo.swift` | — |
| Plasma | `ft-demos/src/plasma.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/PlasmaDemo.swift` | `demos/plasma.py` |
| Quilt | `ft-demos/src/quilt.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/QuiltDemo.swift` | `demos/quilt.py` |
| Random Dots | `ft-demos/src/random-dots.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/RandomDotsDemo.swift` | — |
| SF Logo | — | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/SfLogoDemo.swift` | — |
| Sierpinski | `ft-demos/src/sierpinski.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/SierpinskiDemo.swift` | — |
| Simple Animation | `ft-demos/src/simple-animation.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/SimpleAnimationDemo.swift` | `demos/simple_animation.py` |
| Simple Example | `ft-demos/src/simple-example.cc` | `ft-swift/Sources/FlaschenTaschenDemoKit/Demos/SimpleExampleDemo.swift` | `demos/simple_example.py` |

### How to Port a Demo

1. **Find the Swift reference**: Use the table above to locate the demo in `ft-swift`
2. **Read the Swift code first**: Understand the algorithm and behavior completely
3. **Check the C++ original** (if available): For additional context on algorithms
4. **Implement in Python**: Match the Swift version's behavior exactly
5. **Test thoroughly**: Run the demo and compare visual output with Swift version
