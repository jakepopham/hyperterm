"""Pytest fixtures for hyperterm tests."""

import pytest

from hyperterm import MonospaceGrid, Style


@pytest.fixture
def empty_grid() -> MonospaceGrid:
    """5x5 empty grid for basic tests."""
    return MonospaceGrid(5, 5)


@pytest.fixture
def styled_grid() -> MonospaceGrid:
    """Pre-populated grid with various styles."""
    grid = MonospaceGrid(10, 5)
    grid.draw_text(0, 0, "Hello", fg_color="red", bold=True)
    grid.draw_text(0, 1, "World", fg_color="blue")
    return grid


@pytest.fixture
def default_style() -> Style:
    """Default style instance."""
    return Style()


@pytest.fixture
def red_bold_style() -> Style:
    """Red, bold style."""
    return Style(fg_color="red", bold=True)
