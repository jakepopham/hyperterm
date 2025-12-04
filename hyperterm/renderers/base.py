"""Base renderer protocol for hyperterm."""

from typing import Protocol

from hyperterm.grid import MonospaceGrid


class Renderer(Protocol):
    """Protocol for renderer implementations.

    Any class implementing this protocol can render a MonospaceGrid to a string.
    This enables custom renderer implementations without subclassing.

    Example:
        class CustomRenderer:
            @classmethod
            def render(cls, grid: MonospaceGrid) -> str:
                # Custom rendering logic
                return "custom output"
    """

    @classmethod
    def render(cls, grid: MonospaceGrid) -> str:
        """Render a grid to a string representation.

        Args:
            grid: The MonospaceGrid to render

        Returns:
            String representation of the grid
        """
        ...
