"""Tests for border feature."""

import re
from hyperterm import MonospaceGrid


def test_grid_border_initialization():
    """Test MonospaceGrid border initialization."""
    grid = MonospaceGrid(10, 5, border=True)
    assert grid.border is True
    assert grid.border_padding == 1  # Default padding
    assert grid.border_attrs == {}


def test_grid_border_with_padding():
    """Test MonospaceGrid border with custom padding."""
    grid = MonospaceGrid(10, 5, border=True, border_padding=2)
    assert grid.border_padding == 2


def test_grid_border_with_attrs():
    """Test MonospaceGrid border with attributes."""
    attrs = {"class": "ansi-cyan ansi-bold"}
    grid = MonospaceGrid(10, 5, border=True, border_attrs=attrs)
    assert grid.border_attrs == attrs


def test_grid_no_border_default():
    """Test that border is enabled by default."""
    grid = MonospaceGrid(10, 5)
    assert grid.border is True


# Terminal Renderer Border Tests


def test_terminal_render_without_border():
    """Test that rendering without border works as before."""
    grid = MonospaceGrid(5, 2, border=False)
    grid[0] = "Hello"
    output = grid.to_console()

    # Should not contain border characters
    assert "╭" not in output
    assert "╮" not in output
    assert "│" not in output

    # Should contain content
    clean_output = re.sub(r"\033\[[0-9;]+m", "", output)
    assert "Hello" in clean_output


def test_terminal_render_with_border():
    """Test terminal rendering with border."""
    grid = MonospaceGrid(10, 3, border=True, border_padding=1)
    grid[1, 2:8] = "Test"

    output = grid.to_console()

    # Should contain border characters
    assert "╭" in output
    assert "╮" in output
    assert "╰" in output
    assert "╯" in output
    assert "│" in output
    assert "─" in output

    # Should contain content
    clean_output = re.sub(r"\033\[[0-9;]+m", "", output)
    assert "Test" in clean_output


def test_terminal_render_border_dimensions():
    """Test that border adds correct dimensions."""
    grid = MonospaceGrid(10, 3, border=True, border_padding=1)
    output = grid.to_console()

    lines = output.split("\n")
    # Content: 3 rows
    # Padding: 1 row top + 1 row bottom
    # Border: 1 row top + 1 row bottom
    # Total: 7 rows
    assert len(lines) == 7

    # First line is top border: ╭ + 12 chars (10 content + 2 padding) + ╮
    # Total width = 14 characters
    first_line_clean = re.sub(r"\033\[[0-9;]+m", "", lines[0])
    assert len(first_line_clean) == 14
    assert first_line_clean[0] == "╭"
    assert first_line_clean[-1] == "╮"


def test_terminal_render_border_with_padding_2():
    """Test terminal rendering with border_padding=2."""
    grid = MonospaceGrid(6, 2, border=True, border_padding=2)
    output = grid.to_console()

    lines = output.split("\n")
    # Content: 2 rows
    # Padding: 2 rows top + 2 rows bottom = 4 rows
    # Border: 1 row top + 1 row bottom = 2 rows
    # Total: 2 + 4 + 2 = 8 rows
    assert len(lines) == 8

    # Width = 6 content + 4 padding (2*2) + 2 border = 12 chars
    first_line_clean = re.sub(r"\033\[[0-9;]+m", "", lines[0])
    assert len(first_line_clean) == 12


def test_terminal_render_border_with_attrs():
    """Test terminal rendering with border attributes."""
    attrs = {"class": "ansi-cyan ansi-bold"}
    grid = MonospaceGrid(5, 2, border=True, border_padding=1, border_attrs=attrs)
    output = grid.to_console()

    # Should contain ANSI codes for cyan and bold
    assert "36" in output  # Cyan ANSI code
    assert "1" in output  # Bold ANSI code


def test_terminal_render_border_preserves_content():
    """Test that border rendering preserves content."""
    grid = MonospaceGrid(10, 3, border=True, border_padding=1)
    grid[0] = ("Header", {"class": "ansi-red"})
    grid[1, 2:8] = ("Test", {"class": "ansi-green"})  # 4 chars fits in 6-char slice
    grid[2] = ("Footer", {"class": "ansi-blue"})

    output = grid.to_console()

    # Should contain all content
    clean_output = re.sub(r"\033\[[0-9;]+m", "", output)
    assert "Header" in clean_output
    assert "Test" in clean_output
    assert "Footer" in clean_output

    # Should contain ANSI codes for colors
    assert "31" in output  # Red
    assert "32" in output  # Green
    assert "34" in output  # Blue


# HTML Renderer Border Tests


def test_html_render_without_border():
    """Test HTML rendering without border."""
    grid = MonospaceGrid(5, 2, border=False)
    grid[0] = "Hello"
    output = grid.to_html()

    # Should not contain border characters
    assert "╭" not in output
    assert "╮" not in output
    assert "│" not in output

    # Should contain content
    assert "Hello" in output


def test_html_render_with_border():
    """Test HTML rendering with border."""
    grid = MonospaceGrid(10, 3, border=True, border_padding=1)
    grid[1, 2:8] = "Test"

    output = grid.to_html()

    # Should contain border characters
    assert "╭" in output
    assert "╮" in output
    assert "╰" in output
    assert "╯" in output
    assert "│" in output
    assert "─" in output

    # Should contain content
    assert "Test" in output


def test_html_render_border_dimensions():
    """Test that border adds correct dimensions in HTML."""
    grid = MonospaceGrid(10, 3, border=True, border_padding=1)
    output = grid.to_html()

    # Count the number of lines in the pre tag
    # Extract content between <pre> and </pre>
    content_start = output.find(">", output.find("<pre")) + 1
    content_end = output.find("</pre>")
    content = output[content_start:content_end]

    lines = [line for line in content.split("\n") if line.strip()]
    # Content: 3 rows
    # Padding: 1 row top + 1 row bottom
    # Border: 1 row top + 1 row bottom
    # Total: 7 rows
    assert len(lines) == 7


def test_html_render_border_with_attrs():
    """Test HTML rendering with border attributes."""
    attrs = {"class": "ansi-cyan ansi-bold", "data-border": "fancy"}
    grid = MonospaceGrid(5, 2, border=True, border_padding=1, border_attrs=attrs)
    output = grid.to_html()

    # Should contain the attributes in span tags
    assert 'class="ansi-cyan ansi-bold"' in output or 'class="ansi-bold ansi-cyan"' in output
    assert 'data-border="fancy"' in output


def test_html_render_border_preserves_content():
    """Test that border rendering preserves content in HTML."""
    grid = MonospaceGrid(10, 3, border=True, border_padding=1)
    grid[0] = ("Header", {"class": "ansi-red"})
    grid[1, 2:8] = ("Test", {"class": "ansi-green"})  # 4 chars fits in 6-char slice
    grid[2] = ("Footer", {"class": "ansi-blue"})

    output = grid.to_html()

    # Should contain all content
    assert "Header" in output
    assert "Test" in output
    assert "Footer" in output

    # Should contain HTML attributes
    assert 'class="ansi-red"' in output
    assert 'class="ansi-green"' in output
    assert 'class="ansi-blue"' in output


def test_html_render_border_escapes_html():
    """Test that HTML special characters are escaped in bordered grids."""
    grid = MonospaceGrid(10, 2, border=True, border_padding=1)
    grid[0, 0:5] = "<div>"

    output = grid.to_html()

    # HTML special chars should be escaped
    assert "&lt;div&gt;" in output
    assert "<div>" not in output or output.count("<div>") == 0  # Except in HTML structure


# Integration Tests


def test_border_with_zero_padding():
    """Test border with zero padding."""
    grid = MonospaceGrid(5, 2, border=True, border_padding=0)
    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # Should still have border
    assert "╭" in terminal_output
    assert "╭" in html_output

    # Lines count: 2 content + 0 padding + 2 border = 4
    terminal_lines = terminal_output.split("\n")
    assert len(terminal_lines) == 4


def test_border_grid_indexing_unchanged():
    """Test that grid indexing is unchanged with border enabled."""
    grid = MonospaceGrid(10, 5, border=True, border_padding=1)
    # grid[0, 0] should still refer to first cell of content, not border
    grid[0, 0] = ("X", {"class": "test"})

    assert grid.chars[0][0] == "X"
    assert grid.attrs[0][0] == {"class": "test"}

    # Grid dimensions should be unchanged
    assert grid.width == 10
    assert grid.height == 5


def test_border_empty_grid():
    """Test border rendering on an empty grid."""
    grid = MonospaceGrid(5, 2, border=True, border_padding=1)
    # Don't set any content

    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # Should still render border
    assert "╭" in terminal_output
    assert "╰" in terminal_output
    assert "╭" in html_output
    assert "╰" in html_output
