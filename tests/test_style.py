"""Tests for the Style class."""

import pytest

from hyperterm import Style


def test_style_default_values(default_style: Style):
    """Test Style creation with default values."""
    assert default_style.fg_color == "default"
    assert default_style.bg_color == "default"
    assert default_style.bold is False
    assert default_style.underline is False


def test_style_custom_values():
    """Test Style creation with custom values."""
    style = Style(fg_color="red", bg_color="blue", bold=True, underline=True)
    assert style.fg_color == "red"
    assert style.bg_color == "blue"
    assert style.bold is True
    assert style.underline is True


def test_style_equality():
    """Test Style equality comparison."""
    style1 = Style(fg_color="red", bold=True)
    style2 = Style(fg_color="red", bold=True)
    style3 = Style(fg_color="blue", bold=True)

    assert style1 == style2
    assert style1 != style3


def test_style_is_default(default_style: Style):
    """Test is_default() method."""
    assert default_style.is_default() is True

    styled = Style(fg_color="red")
    assert styled.is_default() is False

    bold_style = Style(bold=True)
    assert bold_style.is_default() is False


def test_style_immutability():
    """Test that Style is immutable (frozen dataclass)."""
    style = Style(fg_color="red")

    with pytest.raises(AttributeError):
        style.fg_color = "blue"  # type: ignore[misc]


def test_style_hash():
    """Test that Style is hashable (can be used in sets/dicts)."""
    style1 = Style(fg_color="red")
    style2 = Style(fg_color="red")
    style3 = Style(fg_color="blue")

    # Should be able to create a set
    style_set = {style1, style2, style3}
    assert len(style_set) == 2  # style1 and style2 are equal


def test_style_all_combinations():
    """Test various combinations of style attributes."""
    # Just foreground
    s1 = Style(fg_color="green")
    assert s1.fg_color == "green"
    assert s1.bg_color == "default"

    # Just background
    s2 = Style(bg_color="yellow")
    assert s2.fg_color == "default"
    assert s2.bg_color == "yellow"

    # Foreground + bold
    s3 = Style(fg_color="red", bold=True)
    assert s3.fg_color == "red"
    assert s3.bold is True

    # Background + underline
    s4 = Style(bg_color="blue", underline=True)
    assert s4.bg_color == "blue"
    assert s4.underline is True

    # All attributes
    s5 = Style(fg_color="white", bg_color="black", bold=True, underline=True)
    assert s5.fg_color == "white"
    assert s5.bg_color == "black"
    assert s5.bold is True
    assert s5.underline is True
