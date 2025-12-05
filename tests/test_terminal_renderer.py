"""Tests for the terminal rendering functionality."""

import re

from hyperterm import MonospaceGrid


def test_attrs_to_ansi_code_default():
    """Test that empty attributes returns empty string."""
    code = MonospaceGrid._attrs_to_ansi_code({})  # type: ignore[reportPrivateUsage]
    assert code == ""


def test_attrs_to_ansi_code_foreground_color():
    """Test ANSI code generation for foreground colors."""
    code = MonospaceGrid._attrs_to_ansi_code({"class": "ansi-red"})  # type: ignore[reportPrivateUsage]
    assert "31" in code  # Red foreground ANSI code


def test_attrs_to_ansi_code_background_color():
    """Test ANSI code generation for background colors."""
    code = MonospaceGrid._attrs_to_ansi_code({"class": "ansi-bg-blue"})  # type: ignore[reportPrivateUsage]
    assert "44" in code  # Blue background ANSI code


def test_attrs_to_ansi_code_bold():
    """Test ANSI code generation for bold text."""
    code = MonospaceGrid._attrs_to_ansi_code({"class": "ansi-bold"})  # type: ignore[reportPrivateUsage]
    assert "1" in code  # Bold ANSI code


def test_attrs_to_ansi_code_underline():
    """Test ANSI code generation for underlined text."""
    code = MonospaceGrid._attrs_to_ansi_code({"class": "ansi-underline"})  # type: ignore[reportPrivateUsage]
    assert "4" in code  # Underline ANSI code


def test_attrs_to_ansi_code_combined():
    """Test ANSI code generation for combined styles."""
    code = MonospaceGrid._attrs_to_ansi_code({"class": "ansi-red ansi-bg-blue ansi-bold ansi-underline"})  # type: ignore[reportPrivateUsage]
    assert "\033[" in code
    assert "31" in code  # Red foreground
    assert "44" in code  # Blue background
    assert "1" in code  # Bold
    assert "4" in code  # Underline


def test_render_empty_grid():
    """Test rendering an empty grid."""
    grid = MonospaceGrid(5, 3, border=False)
    output = grid.to_console()

    # Should contain reset codes
    assert "\033[0m" in output
    # Should have 3 lines
    assert output.count("\n") == 2


def test_render_ansi_format():
    """Test that output contains valid ANSI escape sequences."""
    grid = MonospaceGrid(5, 3, border=False)
    grid[0, 0:2] = ("Hi", {"class": "ansi-red"})
    output = grid.to_console()

    # Check for ANSI escape sequences
    ansi_pattern = r"\033\[[0-9;]+m"
    assert re.search(ansi_pattern, output)

    # Check for reset codes
    assert "\033[0m" in output


def test_render_with_styles():
    """Test rendering grid with various styles."""
    grid = MonospaceGrid(10, 3, border=False)
    grid[0, 0:3] = ("Red", {"class": "ansi-red ansi-bold"})
    grid[1, 0:4] = ("Blue", {"class": "ansi-blue"})

    output = grid.to_console()

    # Should contain text
    assert "Red" in output
    assert "Blue" in output

    # Should contain ANSI codes
    assert "\033[" in output


def test_render_style_transitions():
    """Test that style transitions are handled correctly."""
    grid = MonospaceGrid(10, 1, border=False)
    grid[0, 0:3] = ("ABC", {"class": "ansi-red"})
    grid[0, 3:6] = ("XYZ", {"class": "ansi-blue"})

    output = grid.to_console()

    # Should have multiple ANSI codes for style changes
    assert output.count("\033[") >= 2


def test_render_preserves_characters():
    """Test that all characters are preserved in output."""
    grid = MonospaceGrid(5, 1, border=False)
    text = "Hello"
    grid[0, 0:5] = text

    output = grid.to_console()

    # Remove ANSI codes to check characters
    clean_output = re.sub(r"\033\[[0-9;]+m", "", output)
    assert text in clean_output


def test_render_multiline():
    """Test rendering multiple lines."""
    grid = MonospaceGrid(5, 3, border=False)
    grid[0, 0:5] = "Line1"
    grid[1, 0:5] = "Line2"
    grid[2, 0:5] = "Line3"

    output = grid.to_console()

    # Should have 2 newlines for 3 lines
    assert output.count("\n") == 2

    # All text should be present
    clean_output = re.sub(r"\033\[[0-9;]+m", "", output)
    assert "Line1" in clean_output
    assert "Line2" in clean_output
    assert "Line3" in clean_output


def test_render_resets_at_line_end():
    """Test that styles are reset at the end of each line."""
    grid = MonospaceGrid(5, 2, border=False)
    grid[0, 0:4] = ("Test", {"class": "ansi-red"})

    output = grid.to_console()
    lines = output.split("\n")

    # Each line should end with a reset code
    for line in lines:
        assert line.endswith("\033[0m")


def test_render_with_border():
    """Test rendering grid with border."""
    grid = MonospaceGrid(5, 3, border=True, border_padding=1)
    grid[0, 0:5] = "Test"

    output = grid.to_console()

    # Should contain border characters
    assert "╭" in output
    assert "╰" in output
    assert "│" in output
    assert "─" in output


def test_render_border_with_attrs():
    """Test rendering border with custom attributes."""
    grid = MonospaceGrid(5, 3, border=True, border_attrs={"class": "ansi-cyan"})
    grid[0, 0:5] = "Test"

    output = grid.to_console()

    # Should contain border characters and ANSI codes
    assert "╭" in output
    # Check for cyan color code (36)
    assert "36" in output


def test_str_method():
    """Test that str() calls to_console()."""
    grid = MonospaceGrid(5, 1, border=False)
    grid[0, 0:4] = ("Test", {"class": "ansi-red"})

    output = str(grid)

    # Should contain ANSI codes
    assert "\033[" in output
    assert "Test" in output


def test_repr_method():
    """Test that repr() calls to_console()."""
    grid = MonospaceGrid(5, 1, border=False)
    grid[0, 0:4] = ("Test", {"class": "ansi-red"})

    output = repr(grid)

    # Should contain ANSI codes
    assert "\033[" in output
    assert "Test" in output


def test_parse_classes_to_ansi():
    """Test the class parsing utility function."""
    codes = MonospaceGrid._parse_classes_to_ansi("ansi-red ansi-bold")  # type: ignore[reportPrivateUsage]
    assert "31" in codes  # Red
    assert "1" in codes  # Bold


def test_parse_classes_ignores_non_privileged():
    """Test that non-privileged classes are ignored."""
    codes = MonospaceGrid._parse_classes_to_ansi("ansi-red custom-class ansi-bold")  # type: ignore[reportPrivateUsage]
    # Should only have red and bold, not custom-class
    assert len(codes) == 2
