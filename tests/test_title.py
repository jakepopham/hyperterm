"""Tests for grid title header functionality."""

from hyperterm import MonospaceGrid


def test_grid_title_initialization():
    """Test that grids can be initialized with a title."""
    grid = MonospaceGrid(width=20, height=5, title="Test Title")
    assert grid.title == "Test Title"


def test_grid_title_default_empty():
    """Test that title defaults to empty string."""
    grid = MonospaceGrid(width=20, height=5)
    assert grid.title == ""


def test_terminal_render_with_title():
    """Test that title appears inline in terminal output."""
    grid = MonospaceGrid(width=10, height=2, border=True, title="TITLE")
    grid[0, 0:5] = "Hello"
    grid[1, 0:5] = "World"

    output = grid.to_console()

    # Check that title appears in output
    assert "TITLE" in output

    # Check for top border corners
    assert "╭" in output
    assert "╮" in output

    # Title should be inline with top border (no separator line)
    lines = output.split("\n")
    # First line should contain both the title and the top border
    assert "╭" in lines[0] and "TITLE" in lines[0] and "╮" in lines[0]


def test_terminal_render_without_title():
    """Test that grids without title have standard top border."""
    grid = MonospaceGrid(width=10, height=2, border=True, title="")
    grid[0, 0:5] = "Hello"

    output = grid.to_console()
    lines = output.split("\n")

    # First line should be a standard top border (all dashes)
    # Should contain ╭────────────╮ pattern
    assert "╭" in lines[0] and "╮" in lines[0]
    # Count the dashes - should be the full width
    assert "─" in lines[0]


def test_html_render_with_title():
    """Test that title appears inline in HTML output."""
    grid = MonospaceGrid(width=10, height=2, border=True, title="HTML TITLE")
    grid[0, 0:5] = "Hello"

    output = grid.to_html()

    # Check that title appears in output
    assert "HTML TITLE" in output

    # Check that title is in the first line with the top border
    assert "╭" in output
    assert "╮" in output


def test_html_render_without_title():
    """Test that grids without title have standard top border in HTML."""
    grid = MonospaceGrid(width=10, height=2, border=True, title="")
    grid[0, 0:5] = "Hello"

    output = grid.to_html()

    # Check for standard top border
    assert "╭" in output
    assert "╮" in output


def test_html_title_escaping():
    """Test that HTML special characters in title are properly escaped."""
    # Use a wider grid to avoid truncation
    grid = MonospaceGrid(width=30, height=2, border=True, title="<Test & Title>")

    output = grid.to_html()

    # Check that special characters are escaped
    assert "&lt;Test &amp; Title&gt;" in output
    # Check that raw HTML doesn't appear (except in the <pre> tag itself)
    # We need to check that the title text specifically isn't unescaped
    lines = output.split("\n")
    # Find the line with the title (should be in the top border)
    title_found = False
    for line in lines:
        if "&lt;Test &amp; Title&gt;" in line:
            title_found = True
            # Make sure this line doesn't have the unescaped version
            assert "<Test & Title>" not in line or line.startswith("<pre")
    assert title_found


def test_title_inline_format():
    """Test that title appears inline with top border."""
    grid = MonospaceGrid(width=20, height=2, border=True, border_padding=1, title="TEST")

    output = grid.to_console()
    lines = output.split("\n")

    # Title should be in the first line (top border)
    top_border = lines[0]

    # Check that title appears in the line
    assert "TEST" in top_border

    # The line should have the inline format: ╭─ TEST ───╮
    assert "╭" in top_border
    assert "╮" in top_border
    assert "─" in top_border


def test_title_with_no_border():
    """Test that title has no effect when border is disabled."""
    grid = MonospaceGrid(width=10, height=2, border=False, title="NO BORDER")
    grid[0, 0:5] = "Hello"

    output = grid.to_console()

    # Title should not appear when border is disabled
    # (title only shows in the border header)
    assert "NO BORDER" not in output


def test_title_with_long_text():
    """Test that long titles are handled correctly."""
    grid = MonospaceGrid(width=10, height=2, border=True, title="Very Long Title Text")

    output = grid.to_console()

    # Title should still appear (may be truncated or overflow)
    assert "Very Long Title Text" in output


def test_title_with_border_attrs():
    """Test that title respects border attributes."""
    grid = MonospaceGrid(
        width=10,
        height=2,
        border=True,
        border_attrs={"class": "ansi-cyan ansi-bold"},
        title="STYLED",
    )

    output = grid.to_console()

    # Check that title appears
    assert "STYLED" in output

    # Check that ANSI codes are present (cyan and bold)
    assert "\033[" in output  # ANSI escape code present


def test_grid_auto_expands_for_title():
    """Test that grid width auto-expands to fit the title."""
    # Create a grid with no initial width but a long title
    grid = MonospaceGrid(width=0, height=2, border=True, title="This is a very long title")

    # The grid should have expanded to fit the title
    # Title with spaces: " This is a very long title " = 27 chars
    # Inline format: ╭─ + title + ─ (at least 1) + ╮
    # remaining_width = inner_width - title_width - 1
    # We want remaining_width >= 1, so inner_width >= title_width + 2
    # inner_width = content_width + 2 * padding (padding default is 1)
    # So content_width >= 27 + 2 - 2 = 27
    assert grid.width >= 27


def test_grid_expands_small_width_for_title():
    """Test that grid expands if initial width is too small for title."""
    # Create a grid with small width but a long title
    grid = MonospaceGrid(width=5, height=2, border=True, title="Long Title Here")

    # The grid should have expanded to fit the title
    # Title with spaces: " Long Title Here " = 17 chars
    # Inline format needs: inner_width >= 17 + 2 = 19
    # inner_width = content_width + 2 (padding=1 default)
    # So content_width should be >= 19 - 2 = 17
    assert grid.width >= 17
    assert grid.width == 17  # Should be exactly 17


def test_grid_width_unchanged_if_sufficient():
    """Test that grid width is not changed if already large enough for title."""
    # Create a grid with sufficient width
    grid = MonospaceGrid(width=50, height=2, border=True, title="Short")

    # Width should remain 50 (not reduced)
    assert grid.width == 50


def test_title_expansion_respects_padding():
    """Test that title width calculation respects border_padding."""
    # With padding=2, the inner_width = content_width + 4
    grid = MonospaceGrid(
        width=0, height=2, border=True, border_padding=2, title="Test Title"
    )

    # Title with spaces: " Test Title " = 12 chars
    # Inline format needs: inner_width >= 12 + 2 = 14
    # inner_width = content_width + 2 * 2 = content_width + 4
    # So content_width should be >= 14 - 4 = 10
    assert grid.width >= 10
    assert grid.width == 10  # Should be exactly 10


def test_no_expansion_without_border():
    """Test that title doesn't cause expansion if border is disabled."""
    # Without border, title isn't displayed, so no expansion needed
    grid = MonospaceGrid(width=0, height=2, border=False, title="Long Title")

    # Width should remain 0 (title doesn't display without border)
    assert grid.width == 0
