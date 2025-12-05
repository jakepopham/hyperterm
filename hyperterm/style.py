"""Style class for representing character styling."""

from dataclasses import dataclass

from hyperterm.types import ColorName


@dataclass(frozen=True)
class Style:
    """Represents the style applied to a single character.

    This is an immutable dataclass that defines foreground/background colors
    and text decorations (bold, underline).

    Attributes:
        fg_color: Foreground color name
        bg_color: Background color name
        bold: Whether the text is bold
        underline: Whether the text is underlined
    """

    fg_color: ColorName = "default"
    bg_color: ColorName = "default"
    bold: bool = False
    underline: bool = False

    def is_default(self) -> bool:
        """Check if this style is the default (no styling applied).

        Returns:
            True if all style attributes are at their default values
        """
        return self == Style()
