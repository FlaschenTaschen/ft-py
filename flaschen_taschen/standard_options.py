"""Standard command-line options shared across all demos and tools."""

import argparse
import os
from typing import List, Optional


class StandardOptions:
    """Standard options parser for FlaschenTaschen demos.

    Handles common arguments:
    - -h/--host: Display hostname/IP (default: FT_DISPLAY env var or localhost)
    - -g/--geometry: Display geometry (WxH[+X+Y])
    - -l/--layer: Layer (0-15) (default: 1)
    - -d/--delay: Frame delay (milliseconds) (default: 50)
    - -t/--timeout: Timeout (seconds) (default: 86400)
    """

    def __init__(self, args: Optional[List[str]] = None):
        """Parse standard options from command-line arguments.

        Args:
            args: List of command-line arguments (defaults to sys.argv[1:])
        """
        parser = argparse.ArgumentParser(add_help=False)

        parser.add_argument(
            "-h", "--host",
            default=None,
            help="Display hostname/IP (default: FT_DISPLAY env var or localhost)"
        )
        parser.add_argument(
            "-g", "--geometry",
            default="45x35",
            help="Display geometry: WxH[+X+Y] (default: 45x35)"
        )
        parser.add_argument(
            "-l", "--layer",
            type=int,
            default=1,
            help="Layer 0-15 (default: 1)"
        )
        parser.add_argument(
            "-d", "--delay",
            type=int,
            default=50,
            help="Frame delay in milliseconds (default: 50)"
        )
        parser.add_argument(
            "-t", "--timeout",
            type=int,
            default=86400,
            help="Timeout in seconds (default: 86400 = 24 hours)"
        )

        # Parse only known args, leaving rest for the tool
        parsed, self.non_standard_args = parser.parse_known_args(args)

        # Parse geometry
        self._parse_geometry(parsed.geometry)

        # Store standard options
        self.hostname = parsed.host or os.environ.get("FT_DISPLAY") or "localhost"
        self.layer = parsed.layer
        self.delay = parsed.delay
        self.timeout = parsed.timeout

    def _parse_geometry(self, geom_str: str) -> None:
        """Parse geometry string in format WxH[+X+Y].

        Args:
            geom_str: Geometry string

        Raises:
            ValueError: If geometry string is invalid
        """
        try:
            geom_parts = geom_str.lower().split("+")
            w, h = map(int, geom_parts[0].split("x"))
            x_off = int(geom_parts[1]) if len(geom_parts) > 1 else 0
            y_off = int(geom_parts[2]) if len(geom_parts) > 2 else 0

            if w <= 0 or h <= 0:
                raise ValueError("Width and height must be positive")
            if x_off < 0 or y_off < 0:
                raise ValueError("Offsets must be non-negative")

        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid geometry: {geom_str}") from e

        self.width = w
        self.height = h
        self.xoff = x_off
        self.yoff = y_off

    def __repr__(self) -> str:
        return (
            f"StandardOptions(host={self.hostname}, "
            f"geometry={self.width}x{self.height}+{self.xoff}+{self.yoff}, "
            f"layer={self.layer}, delay={self.delay}ms, timeout={self.timeout}s)"
        )
