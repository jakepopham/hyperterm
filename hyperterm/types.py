"""Type definitions for the hyperterm library."""

from typing import Literal, Protocol, TypedDict

# Color names as Literal types for compile-time checking
ColorName = Literal[
    "red", "green", "blue", "yellow", "black", "white", "cyan", "magenta", "default"
]

# Type aliases for clarity
AnsiCode = str  # ANSI escape code like '31'
HtmlColor = str  # HTML color like '#FF4444'
Coordinate = tuple[int, int]  # (x, y) coordinate


class ColorMapping(TypedDict):
    """Mapping of a color to both ANSI and HTML representations."""

    ansi: AnsiCode
    html: HtmlColor


# Type for the complete color map dictionary
ColorMaps = dict[ColorName, ColorMapping]


class Renderer(Protocol):
    """Protocol for renderer implementations.

    Any class implementing this protocol can render a MonospaceGrid to a string.
    This enables custom renderer implementations without subclassing.
    """

    @classmethod
    def render(cls, grid: "MonospaceGrid") -> str:  # type: ignore[name-defined]
        """Render a grid to a string representation.

        Args:
            grid: The MonospaceGrid to render

        Returns:
            String representation of the grid
        """
        ...
