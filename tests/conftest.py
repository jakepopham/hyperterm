"""Pytest fixtures for hyperterm tests."""

import pytest

from hyperterm import MonospaceGrid


@pytest.fixture
def empty_grid() -> MonospaceGrid:
    """5x5 empty grid for basic tests."""
    return MonospaceGrid(5, 5)
