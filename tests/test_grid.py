"""Tests for the MonospaceGrid class with Pythonic slicing API."""

import pytest
from hyperterm import MonospaceGrid


def test_grid_initialization():
    """Test MonospaceGrid initialization."""
    grid = MonospaceGrid(10, 5, ".")
    assert grid.width == 10
    assert grid.height == 5
    assert grid.fill_char == "."
    assert len(grid.chars) == 5
    assert len(grid.chars[0]) == 10
    assert grid.chars[0][0] == "."


def test_grid_default_fill_char():
    """Test that default fill char is space."""
    grid = MonospaceGrid(3, 3)
    assert grid.fill_char == " "
    assert grid.chars[0][0] == " "


# Tests for setting characters only (string values)


def test_set_single_cell_char():
    """Test setting a single character."""
    grid = MonospaceGrid(5, 5)
    grid[0, 0] = "A"
    assert grid.chars[0][0] == "A"

    grid[2, 3] = "X"
    assert grid.chars[2][3] == "X"


def test_set_single_cell_multichar_string():
    """Test that only first character is used when setting multi-char string."""
    grid = MonospaceGrid(5, 5)
    grid[0, 0] = "ABC"
    assert grid.chars[0][0] == "A"


def test_set_row_with_string():
    """Test setting entire row with string."""
    grid = MonospaceGrid(10, 5)
    grid[0] = "Hello"
    # Should broadcast "Hello" across the 10-cell row
    assert grid.chars[0][0] == "H"
    assert grid.chars[0][1] == "e"
    assert grid.chars[0][2] == "l"
    assert grid.chars[0][3] == "l"
    assert grid.chars[0][4] == "o"
    # Cycles
    assert grid.chars[0][5] == "H"
    assert grid.chars[0][6] == "e"


def test_set_row_slice_with_string():
    """Test setting a row slice with string."""
    grid = MonospaceGrid(10, 5)
    grid[0, 2:7] = "ABC"
    # Should broadcast "ABC" across the 5-cell slice
    assert grid.chars[0][2] == "A"
    assert grid.chars[0][3] == "B"
    assert grid.chars[0][4] == "C"
    assert grid.chars[0][5] == "A"  # Cycles
    assert grid.chars[0][6] == "B"
    # Other cells unchanged
    assert grid.chars[0][0] == " "
    assert grid.chars[0][7] == " "


def test_set_column_with_string():
    """Test setting a column with string."""
    grid = MonospaceGrid(10, 5)
    grid[:, 0] = "XYZ"
    # Should broadcast "XYZ" down the 5-cell column
    assert grid.chars[0][0] == "X"
    assert grid.chars[1][0] == "Y"
    assert grid.chars[2][0] == "Z"
    assert grid.chars[3][0] == "X"  # Cycles
    assert grid.chars[4][0] == "Y"


def test_set_2d_region_with_string():
    """Test setting a 2D region with string."""
    grid = MonospaceGrid(10, 10)
    grid[0:2, 0:3] = "AB"
    # Should broadcast "AB" across 6 cells (2 rows x 3 cols)
    assert grid.chars[0][0] == "A"
    assert grid.chars[0][1] == "B"
    assert grid.chars[0][2] == "A"
    assert grid.chars[1][0] == "B"
    assert grid.chars[1][1] == "A"
    assert grid.chars[1][2] == "B"


# Tests for setting attributes only (dict values)


def test_set_single_cell_attrs():
    """Test setting attributes for a single cell."""
    grid = MonospaceGrid(5, 5)
    grid[0, 0] = {"class": "ansi-red"}
    assert grid.attrs[0][0] == {"class": "ansi-red"}


def test_set_attrs_merges_with_existing():
    """Test that setting attrs merges with existing attrs."""
    grid = MonospaceGrid(5, 5)
    grid[0, 0] = {"class": "ansi-red"}
    grid[0, 0] = {"data-id": "123"}
    # Should merge, not replace
    assert grid.attrs[0][0] == {"class": "ansi-red", "data-id": "123"}


def test_set_row_attrs():
    """Test setting attributes for entire row."""
    grid = MonospaceGrid(10, 5)
    grid[0] = {"class": "ansi-bold"}
    # Should apply to all cells in row
    for col in range(10):
        assert grid.attrs[0][col] == {"class": "ansi-bold"}


def test_set_slice_attrs():
    """Test setting attributes for a slice."""
    grid = MonospaceGrid(10, 5)
    grid[0, 2:5] = {"class": "ansi-cyan"}
    # Should apply to slice only
    assert grid.attrs[0][2] == {"class": "ansi-cyan"}
    assert grid.attrs[0][3] == {"class": "ansi-cyan"}
    assert grid.attrs[0][4] == {"class": "ansi-cyan"}
    # Other cells unchanged
    assert grid.attrs[0][0] == {}
    assert grid.attrs[0][5] == {}


def test_set_column_attrs():
    """Test setting attributes for a column."""
    grid = MonospaceGrid(10, 5)
    grid[:, 0] = {"class": "ansi-green"}
    # Should apply to all cells in column
    for row in range(5):
        assert grid.attrs[row][0] == {"class": "ansi-green"}


# Tests for setting both (tuple values)


def test_set_single_cell_both():
    """Test setting both char and attrs for single cell."""
    grid = MonospaceGrid(5, 5)
    grid[0, 0] = ("X", {"class": "ansi-red"})
    assert grid.chars[0][0] == "X"
    assert grid.attrs[0][0] == {"class": "ansi-red"}


def test_set_row_both():
    """Test setting both chars and attrs for entire row."""
    grid = MonospaceGrid(10, 5)
    grid[0] = ("Hello", {"class": "ansi-bold"})
    # Check chars broadcast
    assert grid.chars[0][0] == "H"
    assert grid.chars[0][5] == "H"  # Cycles
    # Check attrs applied to all
    for col in range(10):
        assert grid.attrs[0][col] == {"class": "ansi-bold"}


def test_set_slice_both():
    """Test setting both chars and attrs for a slice."""
    grid = MonospaceGrid(10, 5)
    grid[0, 2:5] = ("ABC", {"class": "ansi-yellow"})
    # Check chars
    assert grid.chars[0][2] == "A"
    assert grid.chars[0][3] == "B"
    assert grid.chars[0][4] == "C"
    # Check attrs
    assert grid.attrs[0][2] == {"class": "ansi-yellow"}
    assert grid.attrs[0][3] == {"class": "ansi-yellow"}
    assert grid.attrs[0][4] == {"class": "ansi-yellow"}


# Tests for getting values


def test_get_single_cell():
    """Test getting a single cell returns (char, attrs) tuple."""
    grid = MonospaceGrid(5, 5)
    grid[0, 0] = ("X", {"class": "red"})
    chars, attrs = grid[0, 0]
    assert chars == "X"
    assert attrs == {"class": "red"}


def test_get_row():
    """Test getting a row returns (chars_string, attrs_list) tuple."""
    grid = MonospaceGrid(5, 3)
    grid[0] = ("Hello", {"class": "bold"})
    chars, attrs = grid[0]
    assert chars == "Hello"  # Broadcasts to full width
    assert len(attrs) == 5
    assert all(attr == {"class": "bold"} for attr in attrs)


def test_get_slice():
    """Test getting a slice."""
    grid = MonospaceGrid(10, 5)
    grid[0, 2:5] = ("ABC", {"class": "test"})
    chars, attrs = grid[0, 2:5]
    assert chars == "ABC"
    assert len(attrs) == 3
    assert all(attr == {"class": "test"} for attr in attrs)


def test_get_column():
    """Test getting a column."""
    grid = MonospaceGrid(5, 3)
    grid[:, 0] = ("XYZ", {"class": "col"})
    chars, attrs = grid[:, 0]
    assert chars == "XYZ"
    assert len(attrs) == 3
    assert all(attr == {"class": "col"} for attr in attrs)


# Edge cases and error handling


def test_index_out_of_bounds_raises():
    """Test that out of bounds indexing raises IndexError."""
    grid = MonospaceGrid(5, 5)
    with pytest.raises(IndexError):
        grid[10, 0] = "X"
    with pytest.raises(IndexError):
        grid[0, 10] = "X"
    with pytest.raises(IndexError):
        _ = grid[10, 0]


def test_invalid_value_type_raises():
    """Test that invalid value types raise TypeError."""
    grid = MonospaceGrid(5, 5)
    with pytest.raises(TypeError):
        grid[0, 0] = 123  # Not str, dict, or tuple
    with pytest.raises(TypeError):
        grid[0, 0] = ["list"]  # Not valid type


def test_invalid_tuple_raises():
    """Test that invalid tuples raise errors."""
    grid = MonospaceGrid(5, 5)
    with pytest.raises(ValueError):
        grid[0, 0] = ("one",)  # Tuple too short
    with pytest.raises(ValueError):
        grid[0, 0] = ("one", "two", "three")  # Tuple too long
    with pytest.raises(TypeError):
        grid[0, 0] = (123, {"class": "red"})  # First element not string
    with pytest.raises(TypeError):
        grid[0, 0] = ("text", "not-a-dict")  # Second element not dict


def test_empty_string_uses_fill_char():
    """Test that empty string falls back to fill char."""
    grid = MonospaceGrid(5, 5, ".")
    grid[0, 0] = ""
    assert grid.chars[0][0] == " "  # Empty string uses space


def test_negative_slicing():
    """Test that negative slicing works as expected."""
    grid = MonospaceGrid(10, 5)
    grid[0, -3:] = "END"
    assert grid.chars[0][7] == "E"
    assert grid.chars[0][8] == "N"
    assert grid.chars[0][9] == "D"


# Integration tests


def test_complex_grid_operations():
    """Test a complex sequence of operations."""
    grid = MonospaceGrid(20, 10, ".")

    # Draw border
    grid[0] = ("#" * 20, {"class": "ansi-yellow"})
    grid[9] = ("#" * 20, {"class": "ansi-yellow"})
    grid[:, 0] = ("#", {"class": "ansi-yellow"})
    grid[:, 19] = ("#", {"class": "ansi-yellow"})

    # Draw title
    grid[2, 5:15] = ("TITLE", {"class": "ansi-red ansi-bold"})

    # Draw content
    grid[4, 2:18] = ("Content here", {"class": "ansi-white"})

    # Verify
    assert grid.chars[0][0] == "#"
    assert grid.attrs[0][0] == {"class": "ansi-yellow"}
    assert grid.chars[2][5] == "T"
    assert grid.attrs[2][5] == {"class": "ansi-red ansi-bold"}
    chars, _ = grid[4, 2:18]
    assert chars.startswith("Content here")
