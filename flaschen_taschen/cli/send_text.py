"""Send text to FlaschenTaschen display."""

import argparse
import os
import sys
from flaschen_taschen.generators.text import send_text
from flaschen_taschen.client.color import Color


def parse_geometry(geom_str):
    """
    Parse geometry string in format: WxH[+X+Y].

    Returns:
        Tuple (width, height, x_offset, y_offset)
    """
    # Handle WxH+X+Y format
    if '+' in geom_str:
        geom_part, offset_part = geom_str.split('+', 1)
        x_offset = int(offset_part.split('+')[0]) if '+' in offset_part else int(offset_part)
        y_offset = int(offset_part.split('+')[1]) if '+' in offset_part else 0
    else:
        geom_part = geom_str
        x_offset = 0
        y_offset = 0

    width, height = map(int, geom_part.split('x'))
    return (width, height, x_offset, y_offset)


def find_font_file(font_spec):
    """
    Resolve font file path.

    Args:
        font_spec: Path to .bdf font file (absolute or relative)

    Returns:
        Resolved path to font file

    Raises:
        FileNotFoundError: If font file cannot be found
    """
    if os.path.exists(font_spec):
        return os.path.abspath(font_spec)

    raise FileNotFoundError(f"Font file not found: {font_spec}")


def main():
    parser = argparse.ArgumentParser(
        description='Send text to FlaschenTaschen display',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
        epilog='''
Examples:
  send-text -g 45x35 -f 5x5 "Hello World"
  send-text -g 45x35 -h 192.168.1.100 -f 6x12 -c ff0000 "Red Text"
  send-text -g 45x35 -f 5x7 --no-scroll "Static Text"
        ''',
    )

    parser.add_argument('text', help='Text to display')
    parser.add_argument('-g', '--geometry', default='45x35',
                        help='Display geometry WxH[+X+Y] (default: 45x35)')
    parser.add_argument('-h', '--host', default='localhost',
                        help='Display hostname/IP (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=1337,
                        help='Display port (default: 1337)')
    parser.add_argument('-f', '--font', default='5x5.bdf',
                        help='Path to .bdf font file (absolute or relative). Default: 5x5.bdf')
    parser.add_argument('-l', '--layer', type=int, default=0,
                        help='Layer 0-15 (default: 0)')
    parser.add_argument('-c', '--color', default='ffffff',
                        help='Color as hex RGB (default: ffffff)')
    parser.add_argument('--no-scroll', action='store_true',
                        help='Disable scrolling (static text)')
    parser.add_argument('-d', '--delay', type=int, default=0,
                        help='Frame delay in milliseconds (default: 0)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                        help='Connection timeout in seconds (default: 10)')

    args = parser.parse_args()

    try:
        # Parse geometry
        geometry = parse_geometry(args.geometry)

        # Find font file
        font_path = find_font_file(args.font)

        # Parse color
        try:
            color = Color(args.color)
        except ValueError:
            print(f"Error: Invalid color '{args.color}' (use hex like ff0000)", file=sys.stderr)
            return 1

        # Validate layer
        if not 0 <= args.layer <= 15:
            print("Error: Layer must be 0-15", file=sys.stderr)
            return 1

        # Send text
        send_text(
            host=args.host,
            port=args.port,
            geometry=geometry,
            text=args.text,
            font_path=font_path,
            color=color,
            layer=args.layer,
            delay_ms=args.delay,
            timeout_s=args.timeout,
            scroll=not args.no_scroll,
        )

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
