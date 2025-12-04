"""Hyperterm: Unified text rendering for terminal and web.

A type-safe library for creating styled character grids that can be rendered
to both ANSI terminal output and HTML.

Example:
    >>> from hyperterm import MonospaceGrid, TerminalRenderer
    >>> grid = MonospaceGrid(20, 5)
    >>> grid.draw_text(0, 0, "Hello, World!", fg_color="red", bold=True)
    >>> print(TerminalRenderer.render(grid))
"""

from hyperterm.grid import MonospaceGrid
from hyperterm.renderers import HTMLRenderer, TerminalRenderer
from hyperterm.style import Style
from hyperterm.types import ColorName

__all__ = [
    "Style",
    "MonospaceGrid",
    "TerminalRenderer",
    "HTMLRenderer",
    "ColorName",
]

__version__ = "0.1.0"
