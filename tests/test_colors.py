"""Tests for color constants and mappings."""

from hyperterm.colors import COLOR_MAP, BG_COLOR_MAP, AnsiColors


def test_ansi_colors_constants():
    """Test that all ANSI color constants are valid strings."""
    assert isinstance(AnsiColors.FG_RED, str)
    assert isinstance(AnsiColors.FG_GREEN, str)
    assert isinstance(AnsiColors.FG_BLUE, str)
    assert isinstance(AnsiColors.BG_RED, str)
    assert isinstance(AnsiColors.BOLD, str)
    assert isinstance(AnsiColors.UNDERLINE, str)
    assert isinstance(AnsiColors.RESET, str)


def test_color_map_structure():
    """Test that COLOR_MAP has all expected keys and proper structure."""
    expected_colors = ["red", "green", "blue", "yellow", "black", "white", "default"]

    for color in expected_colors:
        assert color in COLOR_MAP
        assert "ansi" in COLOR_MAP[color]
        assert "html" in COLOR_MAP[color]
        assert isinstance(COLOR_MAP[color]["ansi"], str)
        assert isinstance(COLOR_MAP[color]["html"], str)


def test_bg_color_map_structure():
    """Test that BG_COLOR_MAP has all expected keys and proper structure."""
    expected_colors = ["red", "green", "blue", "yellow", "black", "white", "default"]

    for color in expected_colors:
        assert color in BG_COLOR_MAP
        assert "ansi" in BG_COLOR_MAP[color]
        assert "html" in BG_COLOR_MAP[color]
        assert isinstance(BG_COLOR_MAP[color]["ansi"], str)
        assert isinstance(BG_COLOR_MAP[color]["html"], str)


def test_ansi_code_formats():
    """Test that ANSI codes follow expected format."""
    # ANSI codes should be numeric strings
    assert COLOR_MAP["red"]["ansi"] == "31"
    assert COLOR_MAP["green"]["ansi"] == "32"
    assert BG_COLOR_MAP["red"]["ansi"] == "41"


def test_html_color_formats():
    """Test that HTML colors follow expected format."""
    # HTML colors should start with # (except 'inherit')
    assert COLOR_MAP["red"]["html"].startswith("#")
    assert BG_COLOR_MAP["red"]["html"].startswith("#")
    # Default can be 'inherit'
    assert COLOR_MAP["default"]["html"] == "inherit"


def test_default_color_exists():
    """Test that 'default' color exists in both maps."""
    assert "default" in COLOR_MAP
    assert "default" in BG_COLOR_MAP
