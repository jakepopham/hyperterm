"""Tests for the HTML rendering functionality."""

from hyperterm import MonospaceGrid


def test_render_empty_grid():
    """Test rendering an empty grid."""
    grid = MonospaceGrid(5, 3, border=False)
    output = grid.to_html()

    # Should be wrapped in <pre> tag
    assert "<pre" in output
    assert "</pre>" in output

    # Should contain CSS styles
    assert "style=" in output
    assert "font-family:" in output


def test_render_html_structure():
    """Test that output has proper HTML structure."""
    grid = MonospaceGrid(5, 1, border=False)
    output = grid.to_html()

    # Should have <pre> wrapper
    assert output.startswith("<pre")
    assert output.endswith("</pre>")


def test_render_escapes_special_chars():
    """Test that HTML special characters are escaped."""
    grid = MonospaceGrid(5, 1, border=False)
    grid[0, 0] = "<"
    grid[0, 1] = ">"
    grid[0, 2] = "&"

    output = grid.to_html()

    assert "&lt;" in output
    assert "&gt;" in output
    assert "&amp;" in output


def test_render_with_styles():
    """Test rendering grid with various styles."""
    grid = MonospaceGrid(10, 3, border=False)
    grid[0, 0:3] = ("Red", {"class": "ansi-red ansi-bold"})
    grid[1, 0:4] = ("Blue", {"class": "ansi-blue"})

    output = grid.to_html()

    # Should contain text
    assert "Red" in output
    assert "Blue" in output

    # Should contain span tags with styles
    assert "<span" in output
    assert "class=" in output


def test_render_span_tags():
    """Test that styled text is wrapped in span tags."""
    grid = MonospaceGrid(5, 1, border=False)
    grid[0, 0:4] = ("Test", {"class": "ansi-red"})

    output = grid.to_html()

    # Should have opening and closing span
    assert "<span" in output
    assert "</span>" in output


def test_render_style_transitions():
    """Test that style transitions create new spans."""
    grid = MonospaceGrid(10, 1, border=False)
    grid[0, 0:3] = ("ABC", {"class": "ansi-red"})
    grid[0, 3:6] = ("XYZ", {"class": "ansi-blue"})

    output = grid.to_html()

    # Should have multiple spans for different styles
    assert output.count("<span") >= 2
    assert output.count("</span>") >= 2


def test_render_default_background():
    """Test that default background color is applied."""
    grid = MonospaceGrid(5, 1, border=False)
    output = grid.to_html()

    # Should contain default black background
    assert "#000000" in output


def test_render_custom_background():
    """Test that custom background color is applied."""
    grid = MonospaceGrid(5, 1, border=False)
    output = grid.to_html(default_bg="#FF0000")

    # Should contain custom red background
    assert "#FF0000" in output


def test_render_preserves_characters():
    """Test that all characters are preserved in output."""
    grid = MonospaceGrid(5, 1, border=False)
    text = "Hello"
    grid[0, 0:5] = text

    output = grid.to_html()
    assert text in output


def test_render_multiline():
    """Test rendering multiple lines."""
    grid = MonospaceGrid(5, 3, border=False)
    grid[0, 0:5] = "Line1"
    grid[1, 0:5] = "Line2"
    grid[2, 0:5] = "Line3"

    output = grid.to_html()

    # All text should be present
    assert "Line1" in output
    assert "Line2" in output
    assert "Line3" in output


def test_render_closes_spans_at_line_end():
    """Test that spans are closed at the end of each line."""
    grid = MonospaceGrid(5, 2, border=False)
    grid[0, 0:4] = ("Test", {"class": "ansi-red"})
    grid[1, 0:4] = ("Next", {"class": "ansi-blue"})

    output = grid.to_html()

    # Should have equal number of opening and closing span tags
    assert output.count("<span") == output.count("</span>")


def test_render_css_properties():
    """Test that pre tag has expected CSS properties."""
    grid = MonospaceGrid(5, 1, border=False)
    output = grid.to_html()

    # Check for key CSS properties
    assert "font-family:" in output
    assert "monospace" in output
    assert "font-size:" in output
    assert "background-color:" in output
    assert "white-space: pre" in output


def test_render_ampersand_escaping_order():
    """Test that ampersands are escaped before other characters."""
    grid = MonospaceGrid(10, 1, border=False)
    grid[0, 0] = "&"
    grid[0, 1] = "<"

    output = grid.to_html()

    # Should not have double-escaped characters
    assert "&amp;lt;" not in output
    assert "&amp;" in output
    assert "&lt;" in output


def test_render_with_border():
    """Test rendering grid with border."""
    grid = MonospaceGrid(5, 3, border=True, border_padding=1)
    grid[0, 0:5] = "Test"

    output = grid.to_html()

    # Should contain border characters
    assert "╭" in output
    assert "╰" in output
    assert "│" in output
    assert "─" in output


def test_render_border_with_attrs():
    """Test rendering border with custom attributes."""
    grid = MonospaceGrid(5, 3, border=True, border_attrs={"class": "ansi-cyan"})
    grid[0, 0:5] = "Test"

    output = grid.to_html()

    # Should contain border with attributes
    assert "╭" in output
    assert "ansi-cyan" in output


def test_render_custom_html_attrs():
    """Test rendering with custom HTML attributes like HTMX."""
    grid = MonospaceGrid(5, 1, border=False)
    grid[0, 0:4] = ("Link", {"hx-get": "/data", "data-action": "click"})

    output = grid.to_html()

    # Should contain custom attributes
    assert "hx-get" in output
    assert "/data" in output
    assert "data-action" in output
