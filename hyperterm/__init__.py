"""Hyperterm: Unified text rendering for terminal and web.

A type-safe library for creating styled character grids that can be rendered
to both ANSI terminal output and HTML.

Example:
    >>> from hyperterm import MonospaceGrid
    >>> grid = MonospaceGrid(20, 5)
    >>> grid[0, 0:13] = ("Hello, World!", {"class": "ansi-red ansi-bold"})
    >>> print(grid)  # Renders to terminal with ANSI codes
    >>> html = grid.to_html()  # Renders to HTML
"""

from hyperterm.grid import MonospaceGrid

__all__ = [
    "MonospaceGrid",
]

__version__ = "0.1.0"
