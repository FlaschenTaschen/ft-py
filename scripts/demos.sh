#!/bin/sh
# Run FlaschenTaschen demos (compatible with bash, zsh, sh)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Print usage
usage() {
    cat << 'EOF'
Usage: ./scripts/demos.sh [demo_name] [options]

Available demos:
  simple_example     - Static colored rectangles
  simple_animation   - Animated moving circles
  black              - Clear display to black
  plasma             - Smooth plasma effect
  matrix             - Matrix-style falling characters
  blur               - Gaussian blur animation
  quilt              - Procedural quilt pattern
  firefly            - Wandering particles with trails

Options (passed to all demos):
  -h, --host HOST       Display hostname (default: localhost)
  -g, --geometry WxH    Display geometry (default: 45x35)
  -l, --layer LAYER     Layer 0-15 (default: 0)
  -d, --delay MS        Frame delay in milliseconds
  -t, --timeout SECS    Timeout in seconds (default: 10)

Examples:
  ./scripts/demos.sh simple_example
  ./scripts/demos.sh plasma -g 45x35 -t 5
  ./scripts/demos.sh matrix -h display.local -d 50
  ./scripts/demos.sh firefly -t 30

EOF
}

# List all demos
list_demos() {
    echo "Available demos:"
    echo "  simple_example     - Static colored rectangles"
    echo "  simple_animation   - Animated moving circles"
    echo "  black              - Clear display to black"
    echo "  plasma             - Smooth plasma effect"
    echo "  matrix             - Matrix-style falling characters"
    echo "  blur               - Gaussian blur animation"
    echo "  quilt              - Procedural quilt pattern"
    echo "  firefly            - Wandering particles with trails"
}

# Get demo description
get_demo_desc() {
    case "$1" in
        simple_example) echo "Static colored rectangles" ;;
        simple_animation) echo "Animated moving circles" ;;
        black) echo "Clear display to black" ;;
        plasma) echo "Smooth plasma effect" ;;
        matrix) echo "Matrix-style falling characters" ;;
        blur) echo "Gaussian blur animation" ;;
        quilt) echo "Procedural quilt pattern" ;;
        firefly) echo "Wandering particles with trails" ;;
        *) return 1 ;;
    esac
}

# Run a specific demo
run_demo() {
    local demo=$1
    shift

    # Verify demo exists
    if ! get_demo_desc "$demo" > /dev/null 2>&1; then
        echo "Error: Unknown demo '$demo'"
        echo ""
        list_demos
        exit 1
    fi

    if [ ! -f "$SCRIPT_DIR/run_${demo}.sh" ]; then
        echo "Error: Script not found: $SCRIPT_DIR/run_${demo}.sh"
        exit 1
    fi

    desc=$(get_demo_desc "$demo")
    echo "Running: $demo ($desc)"
    "$SCRIPT_DIR/run_${demo}.sh" "$@"
}

# Main
if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    usage
    exit 0
fi

run_demo "$@"
