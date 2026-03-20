"""Color utilities for RGB color handling and palettes."""


class Color:
    """Represents an RGB color with 8-bit channels."""

    # Named color constants
    BLACK = None  # Will be initialized below
    WHITE = None
    RED = None
    GREEN = None
    BLUE = None
    CYAN = None
    MAGENTA = None
    YELLOW = None

    def __init__(self, r, g=None, b=None):
        """Initialize a color from RGB values.

        Args:
            r: Red channel (0-255), or a tuple/list (r, g, b), or another Color
            g: Green channel (0-255)
            b: Blue channel (0-255)
        """
        if isinstance(r, Color):
            self.r = r.r
            self.g = r.g
            self.b = r.b
        elif isinstance(r, (tuple, list)):
            self.r, self.g, self.b = r[0], r[1], r[2]
        elif isinstance(r, str):
            # Parse hex color string (#RRGGBB)
            self.r, self.g, self.b = self._parse_hex(r)
        else:
            self.r = int(r)
            self.g = int(g) if g is not None else 0
            self.b = int(b) if b is not None else 0

        # Clamp values to 0-255
        self.r = max(0, min(255, self.r))
        self.g = max(0, min(255, self.g))
        self.b = max(0, min(255, self.b))

    def _parse_hex(self, hex_string):
        """Parse hex color string (#RRGGBB or RRGGBB)."""
        hex_str = hex_string.lstrip("#")
        if len(hex_str) != 6:
            raise ValueError(f"Invalid hex color: {hex_string}")
        return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)

    def to_hex(self):
        """Convert color to hex string (#RRGGBB)."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def to_tuple(self):
        """Return color as (r, g, b) tuple."""
        return (self.r, self.g, self.b)

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.r == other.r and self.g == other.g and self.b == other.b
        return False

    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"

    def __hash__(self):
        return hash((self.r, self.g, self.b))


# Initialize named color constants
Color.BLACK = Color(0, 0, 0)
Color.WHITE = Color(255, 255, 255)
Color.RED = Color(255, 0, 0)
Color.GREEN = Color(0, 255, 0)
Color.BLUE = Color(0, 0, 255)
Color.CYAN = Color(0, 255, 255)
Color.MAGENTA = Color(255, 0, 255)
Color.YELLOW = Color(255, 255, 0)


class ColorPalette:
    """A collection of colors forming a palette."""

    def __init__(self, colors):
        """Initialize a palette from a list of colors.

        Args:
            colors: List of Color objects
        """
        self.colors = [Color(c) if not isinstance(c, Color) else c for c in colors]

    def get_color(self, index):
        """Get color at index with wrapping."""
        if not self.colors:
            return Color.BLACK
        return self.colors[index % len(self.colors)]

    def __len__(self):
        return len(self.colors)

    def __getitem__(self, index):
        return self.get_color(index)


def create_hsv_palette(num_colors, saturation=1.0, value=1.0):
    """Create a color palette using HSV color space.

    Args:
        num_colors: Number of colors to generate
        saturation: Saturation value (0.0-1.0, default: 1.0)
        value: Value (brightness) (0.0-1.0, default: 1.0)

    Returns:
        ColorPalette with colors distributed across the hue spectrum
    """
    colors = []
    for i in range(num_colors):
        hue = i / num_colors  # 0.0 to 1.0
        rgb = hsv_to_rgb(hue, saturation, value)
        colors.append(Color(*rgb))
    return ColorPalette(colors)


def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB.

    Args:
        h: Hue (0.0-1.0)
        s: Saturation (0.0-1.0)
        v: Value/brightness (0.0-1.0)

    Returns:
        Tuple of (r, g, b) with values 0-255
    """
    h = h % 1.0  # Normalize hue to 0-1
    c = v * s  # Chroma
    h_prime = (h * 6) % 6
    x = c * (1 - abs(h_prime % 2 - 1))

    if h_prime < 1:
        r, g, b = c, x, 0
    elif h_prime < 2:
        r, g, b = x, c, 0
    elif h_prime < 3:
        r, g, b = 0, c, x
    elif h_prime < 4:
        r, g, b = 0, x, c
    elif h_prime < 5:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    m = v - c
    return (
        int((r + m) * 255),
        int((g + m) * 255),
        int((b + m) * 255),
    )


# Predefined palettes
PALETTE_RAINBOW = create_hsv_palette(16)
PALETTE_GRAYSCALE = ColorPalette([Color(i * 16, i * 16, i * 16) for i in range(16)])
