"""ANSI color codes and color mappings for hyperterm."""

from hyperterm.types import ColorMaps


class AnsiColors:
    """Standard ANSI color and style codes."""

    # Foreground colors
    FG_BLACK: str = "30"
    FG_RED: str = "31"
    FG_GREEN: str = "32"
    FG_YELLOW: str = "33"
    FG_BLUE: str = "34"
    FG_MAGENTA: str = "35"
    FG_CYAN: str = "36"
    FG_WHITE: str = "37"

    # Background colors
    BG_BLACK: str = "40"
    BG_RED: str = "41"
    BG_GREEN: str = "42"
    BG_YELLOW: str = "43"
    BG_BLUE: str = "44"
    BG_MAGENTA: str = "45"
    BG_CYAN: str = "46"
    BG_WHITE: str = "47"

    # Styles
    BOLD: str = "1"
    DIM: str = "2"
    UNDERLINE: str = "4"
    RESET: str = "0"


# Foreground color mappings: maps color names to both ANSI and HTML values
COLOR_MAP: ColorMaps = {
    "red": {"ansi": AnsiColors.FG_RED, "html": "#FF4444"},
    "green": {"ansi": AnsiColors.FG_GREEN, "html": "#44FF44"},
    "blue": {"ansi": AnsiColors.FG_BLUE, "html": "#4444FF"},
    "yellow": {"ansi": AnsiColors.FG_YELLOW, "html": "#FFFF44"},
    "black": {"ansi": AnsiColors.FG_BLACK, "html": "#000000"},
    "white": {"ansi": AnsiColors.FG_WHITE, "html": "#FFFFFF"},
    "cyan": {"ansi": AnsiColors.FG_CYAN, "html": "#44FFFF"},
    "magenta": {"ansi": AnsiColors.FG_MAGENTA, "html": "#FF44FF"},
    "default": {"ansi": AnsiColors.FG_WHITE, "html": "inherit"},
}

# Background color mappings
BG_COLOR_MAP: ColorMaps = {
    "red": {"ansi": AnsiColors.BG_RED, "html": "#AA0000"},
    "green": {"ansi": AnsiColors.BG_GREEN, "html": "#00AA00"},
    "blue": {"ansi": AnsiColors.BG_BLUE, "html": "#0000AA"},
    "yellow": {"ansi": AnsiColors.BG_YELLOW, "html": "#AAAA00"},
    "black": {"ansi": AnsiColors.BG_BLACK, "html": "#000000"},
    "white": {"ansi": AnsiColors.BG_WHITE, "html": "#888888"},
    "cyan": {"ansi": AnsiColors.BG_CYAN, "html": "#00AAAA"},
    "magenta": {"ansi": AnsiColors.BG_MAGENTA, "html": "#AA00AA"},
    "default": {"ansi": AnsiColors.BG_BLACK, "html": "inherit"},
}

# Privileged CSS classes that the terminal renderer interprets as ANSI codes
# These can be used in the 'class' attribute of the attributes grid
# The HTML renderer outputs them as regular CSS classes
PRIVILEGED_CLASS_TO_ANSI: dict[str, str] = {
    # Foreground colors
    "ansi-black": AnsiColors.FG_BLACK,
    "ansi-red": AnsiColors.FG_RED,
    "ansi-green": AnsiColors.FG_GREEN,
    "ansi-yellow": AnsiColors.FG_YELLOW,
    "ansi-blue": AnsiColors.FG_BLUE,
    "ansi-magenta": AnsiColors.FG_MAGENTA,
    "ansi-cyan": AnsiColors.FG_CYAN,
    "ansi-white": AnsiColors.FG_WHITE,
    # Background colors
    "ansi-bg-black": AnsiColors.BG_BLACK,
    "ansi-bg-red": AnsiColors.BG_RED,
    "ansi-bg-green": AnsiColors.BG_GREEN,
    "ansi-bg-yellow": AnsiColors.BG_YELLOW,
    "ansi-bg-blue": AnsiColors.BG_BLUE,
    "ansi-bg-magenta": AnsiColors.BG_MAGENTA,
    "ansi-bg-cyan": AnsiColors.BG_CYAN,
    "ansi-bg-white": AnsiColors.BG_WHITE,
    # Text styles
    "ansi-bold": AnsiColors.BOLD,
    "ansi-dim": AnsiColors.DIM,
    "ansi-underline": AnsiColors.UNDERLINE,
}
