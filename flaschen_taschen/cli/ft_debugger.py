"""Simple debugger CLI for FlaschenTaschen displays."""

import sys

from ..client.color import create_hsv_palette
from ..client.config import Config
from ..debugger import DisplayDebugger, Mode
from ..standard_options import StandardOptions


PALETTE_TYPES = {
    "rainbow": lambda: create_hsv_palette(256).colors,
    "greyscale": lambda: [
        __import__('flaschen_taschen.client.color', fromlist=['Color']).Color(i, i, i)
        for i in range(0, 256, 1)
    ],
}


def main(argv=None):
    """Main debugger entry point."""
    # Parse standard options
    try:
        std_opts = StandardOptions(argv)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Parse mode and palette from remaining args
    mode = Mode.EDGES
    palette_name = "rainbow"

    i = 0
    while i < len(std_opts.non_standard_args):
        arg = std_opts.non_standard_args[i]

        if arg == "-m" or arg == "--mode":
            i += 1
            if i < len(std_opts.non_standard_args):
                mode_str = std_opts.non_standard_args[i]
                mode = Mode.FILL if mode_str == "fill" else Mode.EDGES
        elif arg == "-p" or arg == "--palette":
            i += 1
            if i < len(std_opts.non_standard_args):
                palette_name = std_opts.non_standard_args[i]
        elif arg == "--help":
            print_help()
            return 0

        i += 1

    # Validate palette
    if palette_name not in PALETTE_TYPES:
        print(f"Unknown palette: {palette_name}", file=sys.stderr)
        return 1

    # Get palette
    palette = PALETTE_TYPES[palette_name]()

    # Create config from standard options
    config = Config(
        width=std_opts.width,
        height=std_opts.height,
        x_offset=std_opts.xoff,
        y_offset=std_opts.yoff,
        host=std_opts.hostname,
    )

    # Create and run debugger
    debugger = DisplayDebugger(mode=mode, palette=palette, config=config)

    try:
        debugger.run(timeout=std_opts.timeout, delay_ms=std_opts.delay)
    except KeyboardInterrupt:
        print("\nInterrupted")
        return 1

    return 0


def print_help():
    """Print help message."""
    print("""FlaschenTaschen Debugger

Usage: ft-debugger [options] [-m MODE] [-p PALETTE]

Standard Options:
  -h, --host HOST           Display hostname/IP (default: localhost)
  -g, --geometry WxH[+X+Y]  Display geometry (default: 45x35)
  -l, --layer LAYER         Layer 0-15 (default: 0)
  -d, --delay MS            Frame delay in milliseconds (default: 0)
  -t, --timeout SECS        Timeout in seconds (default: 10)

Debugger Options:
  -m, --mode MODE           Mode: edges or fill (default: edges)
  -p, --palette PALETTE     Palette: rainbow or greyscale (default: rainbow)
  --help                    Show this help message

Examples:
  ft-debugger -m edges -t 10
  ft-debugger -m fill -p greyscale -t 5
  ft-debugger -h 192.168.1.100 -g 32x24 -m edges
""")


if __name__ == "__main__":
    sys.exit(main())
