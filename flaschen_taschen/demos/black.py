"""Black demo: Clear the display to black and keep it black.

Ported from ft-swift BlackDemo.
"""

import sys
from flaschen_taschen.client.color import Color
from flaschen_taschen.demos import Demo
from flaschen_taschen.standard_options import StandardOptions


class BlackDemo(Demo):
    """Fill display with black color."""

    def __init__(self, std_opts, use_black=False, use_color=False, color=None, clear_all=False):
        """Initialize demo with options.

        Args:
            std_opts: StandardOptions with parsed CLI arguments
            use_black: Fill with black (1,1,1)
            use_color: Fill with custom color
            color: Color to fill with (default: black)
            clear_all: Clear all layers
        """
        super().__init__(std_opts)
        self.use_black = use_black
        self.use_color = use_color
        self.color = color or Color.BLACK
        self.clear_all = clear_all

    def setup(self) -> None:
        """Initialize canvas and apply fill."""
        super().setup()
        assert self.canvas is not None

        # Fill with color, black, or clear
        if self.use_color:
            self.canvas.fill(self.color)
        elif self.use_black:
            self.canvas.fill(Color(1, 1, 1))
        else:
            self.canvas.clear()

        # Send initial frame
        self.canvas.send()

    def update(self) -> None:
        """No animation."""
        pass

    def draw(self) -> None:
        """Keep display filled/cleared."""
        assert self.canvas is not None

        # Maintain the fill each frame
        if self.use_color:
            self.canvas.fill(self.color)
        elif self.use_black:
            self.canvas.fill(Color(1, 1, 1))
        else:
            self.canvas.clear()


if __name__ == "__main__":
    std_opts = StandardOptions()

    # Parse demo-specific arguments from non_standard_args
    use_black = False
    color = Color.BLACK
    use_color = False
    clear_all = False

    i = 0
    while i < len(std_opts.non_standard_args):
        arg = std_opts.non_standard_args[i]

        if arg.startswith("-"):
            option = arg[1:]

            if option == "b":
                use_black = True
            elif option == "c":
                i += 1
                if i < len(std_opts.non_standard_args):
                    hex_color = std_opts.non_standard_args[i]
                    try:
                        color = Color(hex_color)
                        use_color = True
                    except (ValueError, AttributeError):
                        pass
        elif arg == "all":
            clear_all = True

        i += 1

    demo = BlackDemo(std_opts, use_black=use_black, use_color=use_color, color=color, clear_all=clear_all)
    demo.run()
