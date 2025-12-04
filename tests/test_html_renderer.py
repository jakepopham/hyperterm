"""Tests for the HTMLRenderer."""

from hyperterm import MonospaceGrid, Style
from hyperterm.renderers import HTMLRenderer


def test_get_html_style_default():
    """Test that default style returns empty string."""
    style = Style()
    css = HTMLRenderer._get_html_style(style)
    assert css == ""


def test_get_html_style_foreground_color():
    """Test CSS generation for foreground color."""
    style = Style(fg_color="red")
    css = HTMLRenderer._get_html_style(style)
    assert "color:" in css
    assert "#FF4444" in css


def test_get_html_style_background_color():
    """Test CSS generation for background color."""
    style = Style(bg_color="blue")
    css = HTMLRenderer._get_html_style(style)
    assert "background-color:" in css
    assert "#0000AA" in css


def test_get_html_style_bold():
    """Test CSS generation for bold text."""
    style = Style(bold=True)
    css = HTMLRenderer._get_html_style(style)
    assert "font-weight: bold" in css


def test_get_html_style_underline():
    """Test CSS generation for underlined text."""
    style = Style(underline=True)
    css = HTMLRenderer._get_html_style(style)
    assert "text-decoration: underline" in css


def test_get_html_style_combined():
    """Test CSS generation for combined styles."""
    style = Style(fg_color="red", bg_color="blue", bold=True, underline=True)
    css = HTMLRenderer._get_html_style(style)

    assert "color:" in css
    assert "background-color:" in css
    assert "font-weight: bold" in css
    assert "text-decoration: underline" in css


def test_render_empty_grid():
    """Test rendering an empty grid."""
    grid = MonospaceGrid(5, 3)
    output = HTMLRenderer.render(grid)

    # Should be wrapped in <pre> tag
    assert "<pre" in output
    assert "</pre>" in output

    # Should contain CSS styles
    assert "style=" in output
    assert "font-family:" in output


def test_render_html_structure():
    """Test that output has proper HTML structure."""
    grid = MonospaceGrid(5, 1)
    output = HTMLRenderer.render(grid)

    # Should have <pre> wrapper
    assert output.startswith("<pre")
    assert output.endswith("</pre>")


def test_render_escapes_special_chars():
    """Test that HTML special characters are escaped."""
    grid = MonospaceGrid(5, 1)
    grid.set_char(0, 0, "<")
    grid.set_char(1, 0, ">")
    grid.set_char(2, 0, "&")

    output = HTMLRenderer.render(grid)

    assert "&lt;" in output
    assert "&gt;" in output
    assert "&amp;" in output


def test_render_with_styles():
    """Test rendering grid with various styles."""
    grid = MonospaceGrid(10, 3)
    grid.draw_text(0, 0, "Red", fg_color="red", bold=True)
    grid.draw_text(0, 1, "Blue", fg_color="blue")

    output = HTMLRenderer.render(grid)

    # Should contain text
    assert "Red" in output
    assert "Blue" in output

    # Should contain span tags with styles
    assert "<span" in output
    assert "style=" in output


def test_render_span_tags():
    """Test that styled text is wrapped in span tags."""
    grid = MonospaceGrid(5, 1)
    grid.draw_text(0, 0, "Test", fg_color="red")

    output = HTMLRenderer.render(grid)

    # Should have opening and closing span
    assert "<span" in output
    assert "</span>" in output


def test_render_style_transitions():
    """Test that style transitions create new spans."""
    grid = MonospaceGrid(10, 1)
    grid.draw_text(0, 0, "ABC", fg_color="red")
    grid.draw_text(3, 0, "XYZ", fg_color="blue")

    output = HTMLRenderer.render(grid)

    # Should have multiple spans for different styles
    assert output.count("<span") >= 2
    assert output.count("</span>") >= 2


def test_render_default_background():
    """Test that default background color is applied."""
    grid = MonospaceGrid(5, 1)
    output = HTMLRenderer.render(grid)

    # Should contain default black background
    assert "#000000" in output


def test_render_custom_background():
    """Test that custom background color is applied."""
    grid = MonospaceGrid(5, 1)
    output = HTMLRenderer.render(grid, default_bg="#FF0000")

    # Should contain custom red background
    assert "#FF0000" in output


def test_render_preserves_characters():
    """Test that all characters are preserved in output."""
    grid = MonospaceGrid(5, 1)
    text = "Hello"
    grid.draw_text(0, 0, text)

    output = HTMLRenderer.render(grid)
    assert text in output


def test_render_multiline():
    """Test rendering multiple lines."""
    grid = MonospaceGrid(5, 3)
    grid.draw_text(0, 0, "Line1")
    grid.draw_text(0, 1, "Line2")
    grid.draw_text(0, 2, "Line3")

    output = HTMLRenderer.render(grid)

    # All text should be present
    assert "Line1" in output
    assert "Line2" in output
    assert "Line3" in output


def test_render_closes_spans_at_line_end():
    """Test that spans are closed at the end of each line."""
    grid = MonospaceGrid(5, 2)
    grid.draw_text(0, 0, "Test", fg_color="red")
    grid.draw_text(0, 1, "Next", fg_color="blue")

    output = HTMLRenderer.render(grid)

    # Should have equal number of opening and closing span tags
    assert output.count("<span") == output.count("</span>")


def test_render_css_properties():
    """Test that pre tag has expected CSS properties."""
    grid = MonospaceGrid(5, 1)
    output = HTMLRenderer.render(grid)

    # Check for key CSS properties
    assert "font-family:" in output
    assert "monospace" in output
    assert "font-size:" in output
    assert "background-color:" in output
    assert "white-space: pre" in output


def test_render_box():
    """Test rendering a box."""
    grid = MonospaceGrid(10, 10)
    grid.draw_box(2, 2, 6, 6)

    output = HTMLRenderer.render(grid)

    # Box borders should be present
    assert "#" in output
    # Should have spans for styled borders
    assert "<span" in output


def test_render_ampersand_escaping_order():
    """Test that ampersands are escaped before other characters."""
    grid = MonospaceGrid(10, 1)
    grid.set_char(0, 0, "&")
    grid.set_char(1, 0, "<")

    output = HTMLRenderer.render(grid)

    # Should not have double-escaped characters
    assert "&amp;lt;" not in output
    assert "&amp;" in output
    assert "&lt;" in output
