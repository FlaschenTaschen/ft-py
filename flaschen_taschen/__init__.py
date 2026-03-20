"""FlaschenTaschen Python port - A unified Python package for FT display control."""

__version__ = "0.1.0"
__author__ = "Ported to Python"
__license__ = "MIT"

# Import core client components for easy access
from flaschen_taschen.client import Canvas, Color, Config, PPMFormatter, UDPClient

__all__ = [
    "Canvas",
    "Color",
    "Config",
    "PPMFormatter",
    "UDPClient",
]
