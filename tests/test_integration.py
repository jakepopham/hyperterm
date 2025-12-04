"""Integration tests for hyperterm end-to-end workflows."""

import re

from hyperterm import MonospaceGrid
from hyperterm.renderers import HTMLRenderer, TerminalRenderer


def test_complete_workflow_terminal():
    """Test complete workflow: create → draw → render to terminal."""
    # Create grid
    grid = MonospaceGrid(width=20, height=5, fill_char=".")

    # Draw elements
    grid.draw_box(x=1, y=1, w=18, h=3)
    grid.draw_text(x_start=3, y_start=2, text="Hello, World!", fg_color="red", bold=True)

    # Render to terminal
    output = TerminalRenderer.render(grid)

    # Verify output
    assert "Hello, World!" in output
    assert "\033[" in output  # Has ANSI codes
    assert "\033[0m" in output  # Has reset codes


def test_complete_workflow_html():
    """Test complete workflow: create → draw → render to HTML."""
    # Create grid
    grid = MonospaceGrid(width=20, height=5, fill_char=".")

    # Draw elements
    grid.draw_box(x=1, y=1, w=18, h=3)
    grid.draw_text(x_start=3, y_start=2, text="Hello, World!", fg_color="red", bold=True)

    # Render to HTML
    output = HTMLRenderer.render(grid)

    # Verify output
    assert "Hello, World!" in output
    assert "<pre" in output
    assert "</pre>" in output
    assert "<span" in output


def test_both_renderers_same_grid():
    """Test that both renderers can render the same grid."""
    grid = MonospaceGrid(10, 3)
    grid.draw_text(0, 0, "Test", fg_color="blue")

    terminal_output = TerminalRenderer.render(grid)
    html_output = HTMLRenderer.render(grid)

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
    grid = MonospaceGrid(width=40, height=12, fill_char=".")

    # Draw a colored border box
    grid.draw_box(x=5, y=2, w=30, h=8, char="█")

    # Draw a title in the center (bold, red)
    title = "SYSTEM STATUS"
    x_title = 20 - len(title) // 2
    grid.draw_text(x_start=x_title, y_start=3, text=title, fg_color="red", bold=True)

    # Draw a line of normal text
    grid.draw_text(x_start=7, y_start=5, text="Loading modules...", fg_color="white")

    # Draw a highlighted sequence (green foreground, blue background, underlined)
    grid.draw_text(x_start=7, y_start=7, text="Module BIND_34... ", fg_color="cyan")
    data = "[OK]"
    grid.draw_text(
        x_start=25, y_start=7, text=data, fg_color="green", bg_color="blue", underline=True
    )

    # Draw an error message (yellow text on red background)
    error = "ERROR: MEMORY ACCESS DENIED"
    x_error = 20 - len(error) // 2
    grid.draw_text(
        x_start=x_error, y_start=9, text=error, fg_color="yellow", bg_color="red", bold=True
    )

    # Render both outputs
    terminal_output = TerminalRenderer.render(grid)
    html_output = HTMLRenderer.render(grid)

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
    grid = MonospaceGrid(30, 1)

    # Multiple styled segments in one row
    grid.draw_text(0, 0, "RED", fg_color="red")
    grid.draw_text(4, 0, "BLUE", fg_color="blue", bold=True)
    grid.draw_text(9, 0, "GREEN", fg_color="green", underline=True)

    terminal_output = TerminalRenderer.render(grid)
    html_output = HTMLRenderer.render(grid)

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
    grid = MonospaceGrid(100, 100)

    # Draw some elements
    grid.draw_box(10, 10, 80, 80)
    grid.draw_text(30, 30, "Large Grid Test", fg_color="cyan", bold=True)

    # Should not crash or hang
    terminal_output = TerminalRenderer.render(grid)
    html_output = HTMLRenderer.render(grid)

    # Verify output was generated
    assert len(terminal_output) > 0
    assert len(html_output) > 0
    assert "Large Grid Test" in terminal_output
    assert "Large Grid Test" in html_output


def test_empty_grid_renders():
    """Test that empty grids render without errors."""
    grid = MonospaceGrid(10, 10)

    terminal_output = TerminalRenderer.render(grid)
    html_output = HTMLRenderer.render(grid)

    # Should produce valid output
    assert len(terminal_output) > 0
    assert len(html_output) > 0


def test_single_cell_grid():
    """Test that a 1x1 grid works correctly."""
    grid = MonospaceGrid(1, 1)
    grid.set_char(0, 0, "X")
    grid.set_style(0, 0, fg_color="red", bold=True)

    terminal_output = TerminalRenderer.render(grid)
    html_output = HTMLRenderer.render(grid)

    assert "X" in terminal_output
    assert "X" in html_output


def test_special_characters_in_both_renderers():
    """Test that special characters are handled correctly in both renderers."""
    grid = MonospaceGrid(10, 1)
    grid.draw_text(0, 0, "<>&")

    terminal_output = TerminalRenderer.render(grid)
    html_output = HTMLRenderer.render(grid)

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
    grid = MonospaceGrid(10, 3)

    # Initial render
    grid.draw_text(0, 0, "First", fg_color="red")
    output1 = TerminalRenderer.render(grid)
    assert "First" in output1

    # Modify grid
    grid.draw_text(0, 1, "Second", fg_color="blue")
    output2 = TerminalRenderer.render(grid)
    assert "First" in output2
    assert "Second" in output2

    # Overwrite previous text
    grid.draw_text(0, 0, "Third", fg_color="green")
    output3 = TerminalRenderer.render(grid)
    assert "Third" in output3
    assert "Second" in output3


def test_all_colors():
    """Test rendering with all available colors."""
    colors = ["red", "green", "blue", "yellow", "black", "white"]
    grid = MonospaceGrid(50, len(colors))

    for i, color in enumerate(colors):
        grid.draw_text(0, i, f"{color:10}", fg_color=color, bold=True)  # type: ignore[arg-type]

    terminal_output = TerminalRenderer.render(grid)
    html_output = HTMLRenderer.render(grid)

    # All color names should appear in output
    for color in colors:
        assert color in terminal_output
        assert color in html_output
