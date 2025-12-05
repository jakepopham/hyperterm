"""Integration tests for hyperterm end-to-end workflows."""

import re

from hyperterm import MonospaceGrid


def test_complete_workflow_terminal():
    """Test complete workflow: create → draw → render to terminal."""
    # Create grid
    grid = MonospaceGrid(width=20, height=5, fill_char=".", border=False)

    # Draw border using slicing
    grid[:, 1] = ("|", {"class": "ansi-yellow ansi-bold"})
    grid[:, 18] = ("|", {"class": "ansi-yellow ansi-bold"})
    grid[1, 1:19] = ("-", {"class": "ansi-yellow ansi-bold"})
    grid[3, 1:19] = ("-", {"class": "ansi-yellow ansi-bold"})

    # Draw text
    grid[2, 3:16] = ("Hello, World!", {"class": "ansi-red ansi-bold"})

    # Render to terminal
    output = grid.to_console()

    # Verify output
    assert "Hello, World!" in output
    assert "\033[" in output  # Has ANSI codes
    assert "\033[0m" in output  # Has reset codes


def test_complete_workflow_html():
    """Test complete workflow: create → draw → render to HTML."""
    # Create grid
    grid = MonospaceGrid(width=20, height=5, fill_char=".", border=False)

    # Draw border using slicing
    grid[:, 1] = ("|", {"class": "ansi-yellow ansi-bold"})
    grid[:, 18] = ("|", {"class": "ansi-yellow ansi-bold"})
    grid[1, 1:19] = ("-", {"class": "ansi-yellow ansi-bold"})
    grid[3, 1:19] = ("-", {"class": "ansi-yellow ansi-bold"})

    # Draw text
    grid[2, 3:16] = ("Hello, World!", {"class": "ansi-red ansi-bold"})

    # Render to HTML
    output = grid.to_html()

    # Verify output
    assert "Hello, World!" in output
    assert "<pre" in output
    assert "</pre>" in output
    assert "<span" in output


def test_both_renderers_same_grid():
    """Test that both renderers can render the same grid."""
    grid = MonospaceGrid(10, 3, border=False)
    grid[0, 0:4] = ("Test", {"class": "ansi-blue"})

    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # Both should contain the text
    assert "Test" in terminal_output
    assert "Test" in html_output

    # Terminal should have ANSI codes
    assert "\033[" in terminal_output

    # HTML should have tags
    assert "<" in html_output


def test_demonstrate_grid_workflow():
    """Port of the demonstrate_grid() function from proto.py as a test."""
    # Setup the Grid (40 columns wide, 12 rows tall)
    grid = MonospaceGrid(width=40, height=12, fill_char=".", border=False)

    # Draw a colored border box (5,2 to 35,10)
    # Top and bottom borders
    grid[2, 5:35] = ("█", {"class": "ansi-yellow ansi-bold"})
    grid[9, 5:35] = ("█", {"class": "ansi-yellow ansi-bold"})
    # Left and right borders
    grid[2:10, 5] = ("█", {"class": "ansi-yellow ansi-bold"})
    grid[2:10, 34] = ("█", {"class": "ansi-yellow ansi-bold"})

    # Draw a title in the center (bold, red)
    title = "SYSTEM STATUS"
    x_title = 20 - len(title) // 2
    grid[3, x_title:x_title+len(title)] = (title, {"class": "ansi-red ansi-bold"})

    # Draw a line of normal text
    text1 = "Loading modules..."
    grid[5, 7:7+len(text1)] = (text1, {"class": "ansi-white"})

    # Draw a highlighted sequence (green foreground, blue background, underlined)
    text2 = "Module BIND_34... "
    grid[7, 7:7+len(text2)] = (text2, {"class": "ansi-cyan"})

    data = "[OK]"
    grid[7, 25:25+len(data)] = (data, {"class": "ansi-green ansi-bg-blue ansi-underline"})

    # Draw an error message (yellow text on red background)
    error = "ERROR: MEMORY ACCESS DENIED"
    x_error = 20 - len(error) // 2
    grid[9, x_error:x_error+len(error)] = (error, {"class": "ansi-yellow ansi-bg-red ansi-bold"})

    # Render both outputs
    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # Verify key elements are present in both outputs
    assert "SYSTEM STATUS" in terminal_output
    assert "Loading modules..." in terminal_output
    assert "[OK]" in terminal_output
    assert "ERROR: MEMORY ACCESS DENIED" in terminal_output

    assert "SYSTEM STATUS" in html_output
    assert "Loading modules..." in html_output
    assert "[OK]" in html_output
    assert "ERROR: MEMORY ACCESS DENIED" in html_output


def test_complex_nested_styles():
    """Test complex nested styles in the same row."""
    grid = MonospaceGrid(30, 1, border=False)

    # Multiple styled segments in one row
    grid[0, 0:3] = ("RED", {"class": "ansi-red"})
    grid[0, 4:8] = ("BLUE", {"class": "ansi-blue ansi-bold"})
    grid[0, 9:14] = ("GREEN", {"class": "ansi-green ansi-underline"})

    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # All text should be present
    assert "RED" in terminal_output
    assert "BLUE" in terminal_output
    assert "GREEN" in terminal_output

    assert "RED" in html_output
    assert "BLUE" in html_output
    assert "GREEN" in html_output


def test_large_grid_performance():
    """Test that large grids can be created and rendered."""
    # Create a 100x100 grid
    grid = MonospaceGrid(100, 100, border=False)

    # Draw some elements using slicing API
    # Draw box borders
    grid[10, 10:90] = ("=", {"class": "ansi-yellow ansi-bold"})
    grid[89, 10:90] = ("=", {"class": "ansi-yellow ansi-bold"})
    grid[10:90, 10] = ("|", {"class": "ansi-yellow ansi-bold"})
    grid[10:90, 89] = ("|", {"class": "ansi-yellow ansi-bold"})

    # Draw text
    text = "Large Grid Test"
    grid[30, 30:30+len(text)] = (text, {"class": "ansi-cyan ansi-bold"})

    # Should not crash or hang
    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # Verify output was generated
    assert len(terminal_output) > 0
    assert len(html_output) > 0
    assert "Large Grid Test" in terminal_output
    assert "Large Grid Test" in html_output


def test_empty_grid_renders():
    """Test that empty grids render without errors."""
    grid = MonospaceGrid(10, 10, border=False)

    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # Should produce valid output
    assert len(terminal_output) > 0
    assert len(html_output) > 0


def test_single_cell_grid():
    """Test that a 1x1 grid works correctly."""
    grid = MonospaceGrid(1, 1, border=False)
    grid[0, 0] = ("X", {"class": "ansi-red ansi-bold"})

    terminal_output = grid.to_console()
    html_output = grid.to_html()

    assert "X" in terminal_output
    assert "X" in html_output


def test_special_characters_in_both_renderers():
    """Test that special characters are handled correctly in both renderers."""
    grid = MonospaceGrid(10, 1, border=False)
    grid[0, 0:3] = "<>&"

    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # Terminal should preserve raw characters
    assert "<" in terminal_output
    assert ">" in terminal_output
    assert "&" in terminal_output

    # HTML should escape them
    assert "&lt;" in html_output
    assert "&gt;" in html_output
    assert "&amp;" in html_output


def test_grid_modifications():
    """Test that grid can be modified and re-rendered."""
    grid = MonospaceGrid(10, 3, border=False)

    # Initial render
    grid[0, 0:5] = ("First", {"class": "ansi-red"})
    output1 = grid.to_console()
    assert "First" in output1

    # Modify grid
    grid[1, 0:6] = ("Second", {"class": "ansi-blue"})
    output2 = grid.to_console()
    assert "First" in output2
    assert "Second" in output2

    # Overwrite previous text
    grid[0, 0:5] = ("Third", {"class": "ansi-green"})
    output3 = grid.to_console()
    assert "Third" in output3
    assert "Second" in output3


def test_all_colors():
    """Test rendering with all available colors."""
    colors = ["red", "green", "blue", "yellow", "black", "white"]
    grid = MonospaceGrid(50, len(colors), border=False)

    for i, color in enumerate(colors):
        text = f"{color:10}"
        grid[i, 0:10] = (text, {"class": f"ansi-{color} ansi-bold"})

    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # All color names should appear in output
    for color in colors:
        assert color in terminal_output
        assert color in html_output


def test_grid_with_border():
    """Test that grids with borders work correctly."""
    grid = MonospaceGrid(10, 5, border=True, border_padding=1)
    grid[2, 2:7] = ("Hello", {"class": "ansi-green"})

    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # Should contain border characters
    assert "╭" in terminal_output
    assert "╰" in terminal_output
    assert "│" in terminal_output

    assert "╭" in html_output
    assert "╰" in html_output
    assert "│" in html_output

    # Should contain content
    assert "Hello" in terminal_output
    assert "Hello" in html_output
