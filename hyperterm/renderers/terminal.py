"""Terminal renderer for hyperterm using ANSI escape codes."""

from hyperterm.colors import PRIVILEGED_CLASS_TO_ANSI
from hyperterm.grid import MonospaceGrid


class TerminalRenderer:
    """Renders a MonospaceGrid to a string using ANSI escape codes."""

    @staticmethod
    def _parse_classes_to_ansi(class_str: str) -> list[str]:
        """Parse a space-separated class string and extract ANSI codes.

        Args:
            class_str: Space-separated string of CSS class names

        Returns:
            List of ANSI codes from privileged classes
        """
        if not class_str:
            return []

        codes: list[str] = []
        classes = class_str.split()
        for cls in classes:
            if cls in PRIVILEGED_CLASS_TO_ANSI:
                codes.append(PRIVILEGED_CLASS_TO_ANSI[cls])

        return codes

    @staticmethod
    def _attrs_to_ansi_code(attrs: dict[str, str]) -> str:
        """Convert an attributes dict to an ANSI escape sequence string.

        Only processes the 'class' attribute for privileged classes.

        Args:
            attrs: Dictionary of HTML attributes

        Returns:
            ANSI escape sequence string (e.g., "\\033[31;1m") or empty string
        """
        codes = TerminalRenderer._parse_classes_to_ansi(attrs.get("class", ""))

        if not codes:
            return ""

        return f"\033[{';'.join(codes)}m"

    @classmethod
    def render(cls, grid: MonospaceGrid) -> str:
        """Render the grid to a terminal-friendly string.

        Args:
            grid: The MonospaceGrid to render

        Returns:
            String with ANSI escape codes for terminal output
        """
        output: list[str] = []
        current_attrs: dict[str, str] = {}  # Tracks the currently applied attributes

        for y in range(grid.height):
            line: list[str] = []

            # Start first line with a reset for safety
            if y == 0:
                line.append("\033[0m")

            for x in range(grid.width):
                char = grid.chars[y][x]
                attrs = grid.attrs[y][x]

                if attrs != current_attrs:
                    # Attributes changed: reset and apply new code
                    line.append("\033[0m")
                    line.append(cls._attrs_to_ansi_code(attrs))
                    current_attrs = attrs

                line.append(char)

            # End of row: reset and prepare for next row
            line.append("\033[0m")
            output.append("".join(line))
            # Reset tracking for next row
            current_attrs = {}

        return "\n".join(output)
