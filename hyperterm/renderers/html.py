"""HTML renderer for hyperterm."""

from hyperterm.grid import MonospaceGrid


class HTMLRenderer:
    """Renders a MonospaceGrid to HTML with attributes as HTML attributes."""

    @staticmethod
    def _attrs_to_html_attrs(attrs: dict[str, str]) -> str:
        """Convert an attributes dict to an HTML attribute string.

        Args:
            attrs: Dictionary of HTML attributes

        Returns:
            String like 'class="foo bar" hx-get="/data" style="color: blue"'
        """
        if not attrs:
            return ""

        parts: list[str] = []
        for key, value in sorted(attrs.items()):
            # HTML-escape the value
            safe_value = (
                value.replace("&", "&amp;")
                .replace('"', "&quot;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            parts.append(f'{key}="{safe_value}"')

        return " ".join(parts)

    @classmethod
    def render(cls, grid: MonospaceGrid, default_bg: str = "#000000") -> str:
        """Render the grid to HTML with attributes merged on spans.

        Args:
            grid: The MonospaceGrid to render
            default_bg: Default background color for the <pre> wrapper

        Returns:
            HTML string with attributes on span elements
        """
        output: list[str] = []
        current_attrs: dict[str, str] = {}  # Tracks the currently applied attributes

        for y in range(grid.height):
            line: list[str] = []
            for x in range(grid.width):
                char = grid.chars[y][x]
                attrs = grid.attrs[y][x]

                # HTML-escape the character
                safe_char = (
                    char.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                )

                if attrs != current_attrs:
                    # Close previous span (if one was open)
                    if current_attrs:
                        line.append("</span>")

                    # Open new span if new attrs is not empty
                    if attrs:
                        attrs_str = cls._attrs_to_html_attrs(attrs)
                        line.append(f"<span {attrs_str}>")

                    current_attrs = attrs

                line.append(safe_char)

            # End of row: ensure any open span is closed
            if current_attrs:
                line.append("</span>")

            # Reset attrs tracking for the next line
            current_attrs = {}
            output.append("".join(line))
            output.append("\n")

        # Wrap everything in a <pre> tag for monospaced font and whitespace preservation
        content = "".join(output).strip()

        # Add basic retro CSS for the wrapper <pre> tag
        html_style = f"""
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.1;
            background-color: {default_bg};
            color: #FFFFFF;
            padding: 10px;
            border: 2px solid #555;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
            white-space: pre;
            display: inline-block;
        """
        return f'<pre style="{html_style}">{content}</pre>'
