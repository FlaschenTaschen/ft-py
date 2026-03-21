"""Send image to FlaschenTaschen display."""

import argparse
import sys
import os
from flaschen_taschen.generators.image import send_image


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


def main():
    parser = argparse.ArgumentParser(
        description='Send image to FlaschenTaschen display',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
        epilog='''
Examples:
  send-image -g 45x35 image.png
  send-image -g 45x35 -h 192.168.1.100 photo.jpg
  send-image -g 45x35 -l 2 image.png
        ''',
    )

    parser.add_argument('image', help='Path to image file')
    parser.add_argument('-g', '--geometry', default='45x35',
                        help='Display geometry WxH[+X+Y] (default: 45x35)')
    parser.add_argument('-h', '--host', default='localhost',
                        help='Display hostname/IP (default: localhost)')
    parser.add_argument('-p', '--port', type=int, default=1337,
                        help='Display port (default: 1337)')
    parser.add_argument('-l', '--layer', type=int, default=0,
                        help='Layer 0-15 (default: 0)')
    parser.add_argument('-d', '--delay', type=int, default=0,
                        help='Frame delay in milliseconds (default: 0)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                        help='Connection timeout in seconds (default: 10)')

    args = parser.parse_args()

    try:
        # Check file exists
        if not os.path.exists(args.image):
            print(f"Error: Image file not found: {args.image}", file=sys.stderr)
            return 1

        # Parse geometry
        geometry = parse_geometry(args.geometry)

        # Validate layer
        if not 0 <= args.layer <= 15:
            print("Error: Layer must be 0-15", file=sys.stderr)
            return 1

        # Send image
        send_image(
            host=args.host,
            port=args.port,
            geometry=geometry,
            image_path=args.image,
            layer=args.layer,
            delay_ms=args.delay,
            timeout_s=args.timeout,
        )

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
