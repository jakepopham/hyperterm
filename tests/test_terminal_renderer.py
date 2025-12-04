"""Tests for the TerminalRenderer."""

import re

from hyperterm import MonospaceGrid, Style
from hyperterm.renderers import TerminalRenderer


def test_get_ansi_code_default_style():
    """Test that default style returns empty string."""
    style = Style()
    code = TerminalRenderer._get_ansi_code(style)
    assert code == ""


def test_get_ansi_code_foreground_color():
    """Test ANSI code generation for foreground colors."""
    style = Style(fg_color="red")
    code = TerminalRenderer._get_ansi_code(style)
    assert "31" in code  # Red foreground ANSI code


def test_get_ansi_code_background_color():
    """Test ANSI code generation for background colors."""
    style = Style(bg_color="blue")
    code = TerminalRenderer._get_ansi_code(style)
    assert "44" in code  # Blue background ANSI code


def test_get_ansi_code_bold():
    """Test ANSI code generation for bold text."""
    style = Style(bold=True)
    code = TerminalRenderer._get_ansi_code(style)
    assert "1" in code  # Bold ANSI code


def test_get_ansi_code_underline():
    """Test ANSI code generation for underlined text."""
    style = Style(underline=True)
    code = TerminalRenderer._get_ansi_code(style)
    assert "4" in code  # Underline ANSI code


def test_get_ansi_code_combined():
    """Test ANSI code generation for combined styles."""
    style = Style(fg_color="red", bg_color="blue", bold=True, underline=True)
    code = TerminalRenderer._get_ansi_code(style)
    assert "\033[" in code
    assert "31" in code  # Red foreground
    assert "44" in code  # Blue background
    assert "1" in code  # Bold
    assert "4" in code  # Underline


def test_render_empty_grid():
    """Test rendering an empty grid."""
    grid = MonospaceGrid(5, 3)
    output = TerminalRenderer.render(grid)

    # Should contain reset codes
    assert "\033[0m" in output
    # Should have 3 lines
    assert output.count("\n") == 2


def test_render_ansi_format():
    """Test that output contains valid ANSI escape sequences."""
    grid = MonospaceGrid(5, 3)
    grid.draw_text(0, 0, "Hi", fg_color="red")
    output = TerminalRenderer.render(grid)

    # Check for ANSI escape sequences
    ansi_pattern = r"\033\[[0-9;]+m"
    assert re.search(ansi_pattern, output)

    # Check for reset codes
    assert "\033[0m" in output


def test_render_with_styles():
    """Test rendering grid with various styles."""
    grid = MonospaceGrid(10, 3)
    grid.draw_text(0, 0, "Red", fg_color="red", bold=True)
    grid.draw_text(0, 1, "Blue", fg_color="blue")

    output = TerminalRenderer.render(grid)

    # Should contain text
    assert "Red" in output
    assert "Blue" in output

    # Should contain ANSI codes
    assert "\033[" in output


def test_render_style_transitions():
    """Test that style transitions are handled correctly."""
    grid = MonospaceGrid(10, 1)
    grid.draw_text(0, 0, "ABC", fg_color="red")
    grid.draw_text(3, 0, "XYZ", fg_color="blue")

    output = TerminalRenderer.render(grid)

    # Should have multiple ANSI codes for style changes
    assert output.count("\033[") >= 2


def test_render_preserves_characters():
    """Test that all characters are preserved in output."""
    grid = MonospaceGrid(5, 1)
    text = "Hello"
    grid.draw_text(0, 0, text)

    output = TerminalRenderer.render(grid)

    # Remove ANSI codes to check characters
    clean_output = re.sub(r"\033\[[0-9;]+m", "", output)
    assert text in clean_output


def test_render_multiline():
    """Test rendering multiple lines."""
    grid = MonospaceGrid(5, 3)
    grid.draw_text(0, 0, "Line1")
    grid.draw_text(0, 1, "Line2")
    grid.draw_text(0, 2, "Line3")

    output = TerminalRenderer.render(grid)

    # Should have 2 newlines for 3 lines
    assert output.count("\n") == 2

    # All text should be present
    clean_output = re.sub(r"\033\[[0-9;]+m", "", output)
    assert "Line1" in clean_output
    assert "Line2" in clean_output
    assert "Line3" in clean_output


def test_render_resets_at_line_end():
    """Test that styles are reset at the end of each line."""
    grid = MonospaceGrid(5, 2)
    grid.draw_text(0, 0, "Test", fg_color="red")

    output = TerminalRenderer.render(grid)
    lines = output.split("\n")

    # Each line should end with a reset code
    for line in lines:
        assert line.endswith("\033[0m")


def test_render_box():
    """Test rendering a box with styled borders."""
    grid = MonospaceGrid(10, 10)
    grid.draw_box(2, 2, 6, 6)

    output = TerminalRenderer.render(grid)

    # Box borders are styled yellow and bold by default
    # Output should contain ANSI codes and # characters
    assert "#" in output
    assert "\033[" in output
