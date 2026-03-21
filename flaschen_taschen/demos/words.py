"""
Words - Scrolling text display with color palettes
Ported from words.cc (incomplete) and adapted for Python

Renders text horizontally scrolling across the display with smooth animation.
Supports multiple color palettes for visual effects.
"""

from flaschen_taschen.demos import Demo
from flaschen_taschen.client.color import Color
from flaschen_taschen.utils.bitmap_font import BitmapFont
from flaschen_taschen.standard_options import StandardOptions


class Words(Demo):
    """
    Scrolling text animation with color palettes.

    The demo:
    - Renders text that scrolls horizontally across the display
    - Supports multiple color palettes (Nebula, Fire, Bluegreen)
    - Text scrolls from right to left continuously
    - Each frame advances the scroll position
    """

    def __init__(self, std_opts):
        super().__init__(std_opts)
        self.text = "Hello World"
        self.palette_num = 1  # 1=Nebula, 2=Fire, 3=Bluegreen
        self.scroll_pos = 0

        # Parse demo-specific arguments
        args = std_opts.non_standard_args
        i = 0
        while i < len(args) and args[i].startswith('-'):
            arg = args[i]
            option = arg[1:]

            if option == 'p':
                i += 1
                if i < len(args):
                    try:
                        palette = int(args[i])
                        if 1 <= palette <= 3:
                            self.palette_num = palette
                    except ValueError:
                        pass

            i += 1

        # Collect remaining non-option arguments as text
        if i < len(args):
            self.text = ' '.join(args[i:])

    def setup(self):
        """Initialize font and palette."""
        super().setup()

        self.font = BitmapFont()
        self.palette = self._create_palette(self.palette_num)
        self.fg_color = self.palette[255]  # Use brightest color for text
        self.bg_color = Color(0, 0, 0)  # Black background

        # Calculate text width in pixels
        self.text_width = sum(self.font.char_width(c) + 1 for c in self.text)
        self.total_scroll_width = self.canvas.width + self.text_width

    def update(self):
        """Advance text scroll position."""
        self.scroll_pos = (self.scroll_pos + 1) % self.total_scroll_width

    def draw(self):
        """Draw scrolling text."""
        # Clear canvas
        self.canvas.fill_rect(0, 0, self.canvas.width, self.canvas.height, self.bg_color)

        # Calculate baseline position (vertically centered)
        text_height = self.font.height()
        y_pos = (self.canvas.height - text_height) // 2 + self.font.baseline()

        # Draw text at scroll position
        x_pos = self.canvas.width - self.scroll_pos

        for char in self.text:
            char_width = self.font.char_width(char)

            # Only draw if visible on screen
            if x_pos + char_width >= 0 and x_pos < self.canvas.width:
                self.font.draw_char(
                    self.canvas, char, x_pos, y_pos,
                    self.fg_color, self.bg_color
                )

            x_pos += char_width + 1  # +1 for character spacing

    def _create_palette(self, palette_num):
        """Generate color palette."""
        palette = [Color(0, 0, 0)] * 256

        if palette_num == 1:
            # Nebula: black -> blue -> blue-violet -> red -> white
            self._add_gradient(palette, 0, 63, 0, 0, 0, 0, 0, 127)
            self._add_gradient(palette, 64, 127, 0, 0, 127, 127, 0, 255)
            self._add_gradient(palette, 128, 191, 127, 0, 255, 255, 0, 0)
            self._add_gradient(palette, 192, 255, 255, 0, 0, 255, 255, 255)

        elif palette_num == 2:
            # Fire: black -> blue -> red -> yellow -> white
            self._add_gradient(palette, 0, 63, 0, 0, 0, 0, 0, 127)
            self._add_gradient(palette, 64, 127, 0, 0, 127, 255, 0, 0)
            self._add_gradient(palette, 128, 191, 255, 0, 0, 255, 255, 0)
            self._add_gradient(palette, 192, 255, 255, 255, 0, 255, 255, 255)

        elif palette_num == 3:
            # Bluegreen: black -> blue -> teal -> green -> white
            self._add_gradient(palette, 0, 63, 0, 0, 0, 0, 0, 127)
            self._add_gradient(palette, 64, 127, 0, 0, 127, 0, 127, 255)
            self._add_gradient(palette, 128, 191, 0, 127, 255, 0, 255, 0)
            self._add_gradient(palette, 192, 255, 0, 255, 0, 255, 255, 255)

        return palette

    @staticmethod
    def _add_gradient(palette, start, end, r1, g1, b1, r2, g2, b2):
        """Add a color gradient to the palette."""
        range_val = end - start
        for i in range(range_val + 1):
            k = i / range_val if range_val > 0 else 0
            r = int(r1 + (r2 - r1) * k)
            g = int(g1 + (g2 - g1) * k)
            b = int(b1 + (b2 - b1) * k)
            palette[start + i] = Color(r, g, b)


if __name__ == '__main__':
    from flaschen_taschen.demos import run_demo
    run_demo(Words)
