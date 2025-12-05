"""MonospaceGrid class for character grid manipulation with Pythonic slicing API."""

from typing import Optional, Union
from hyperterm.colors import PRIVILEGED_CLASS_TO_ANSI


class MonospaceGrid:
    """A grid structure for holding characters and their attributes with Pythonic slicing API.

    Coordinates are (row, col) where row is y-axis and col is x-axis.
    (0, 0) is top-left.

    Each cell has:
    - A character (str)
    - Attributes (dict[str, str]) for HTML/styling purposes

    The grid uses intelligent type-based dispatch for indexing:
    - String value: sets characters only
    - Dict value: sets attributes only
    - Tuple (str, dict): sets both characters and attributes

    The grid also supports dynamic sizing and a print() method for console-like output.

    Examples:
        # Create fixed-size grid
        grid = MonospaceGrid(width=80, height=24)

        # Create auto-expanding grid
        grid = MonospaceGrid()
        grid.print("Hello", color="red", bold=True)
        grid.print(" World\n", color="green")

        # Set characters only
        grid[0] = 'Hello World'              # Set row 0
        grid[1, 5] = 'X'                     # Set single char at (1, 5)
        grid[2, 10:20] = 'status'            # Set slice with broadcasting
        grid[:, 0] = '|'                     # Set column (vertical borders)

        # Set attributes only
        grid[0] = {'class': 'ansi-red'}      # Set attrs for entire row
        grid[1, 5:10] = {'class': 'bold'}    # Set attrs for slice

        # Set both at once
        grid[0, :5] = ('TITLE', {'class': 'ansi-yellow ansi-bold'})
        grid[3] = ('=' * 80, {'class': 'ansi-dim'})

        # Get values (always returns tuple of (chars, attrs))
        chars, attrs = grid[0]               # Get entire row
        char, attr = grid[1, 5]              # Get single cell

    Attributes:
        width: Number of columns in the grid
        height: Number of rows in the grid
        fill_char: Character used to fill empty cells
        chars: 2D list of characters
        attrs: 2D list of attribute dictionaries
        cursor_row: Current row position for print() method
        cursor_col: Current column position for print() method
        border: Whether to render a border around the grid
        border_padding: Whitespace between border and content (default: 1)
        border_attrs: HTML attributes for border characters
    """

    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        fill_char: str = " ",
        border: bool = True,
        border_padding: int = 1,
        border_attrs: Optional[dict[str, str]] = None,
    ) -> None:
        """Initialize a new MonospaceGrid.

        Args:
            width: Number of columns (optional, defaults to 0 and auto-expands)
            height: Number of rows (optional, defaults to 0 and auto-expands)
            fill_char: Character to fill the grid with (default: space)
            border: Whether to render a border around the grid (default: False)
            border_padding: Number of whitespace cells between border and content (default: 1)
            border_attrs: HTML attributes to apply to border characters (default: {})
        """
        self.width: int = width if width is not None else 0
        self.height: int = height if height is not None else 0
        self.fill_char: str = fill_char
        self.border: bool = border
        self.border_padding: int = border_padding
        self.border_attrs: dict[str, str] = border_attrs if border_attrs is not None else {}

        # Cursor tracking for print() method
        self.cursor_row: int = 0
        self.cursor_col: int = 0

        # Initialize the grid with fill_char and empty attributes
        self.chars: list[list[str]] = [[fill_char] * self.width for _ in range(self.height)]
        self.attrs: list[list[dict[str, str]]] = [
            [{} for _ in range(self.width)] for _ in range(self.height)
        ]

    def __getitem__(
        self, key: Union[int, tuple[int, ...]]
    ) -> tuple[Union[str, list[str]], Union[dict[str, str], list[dict[str, str]]]]:
        """Get character(s) and attribute(s) from the grid.

        Always returns a tuple of (chars, attrs) regardless of slice type.

        Examples:
            chars, attrs = grid[0]           # Entire row
            char, attr = grid[1, 5]          # Single cell
            chars, attrs = grid[0, 2:5]      # Row slice
            chars, attrs = grid[:, 0]        # Column
        """
        chars = self._get_chars(key)
        attrs = self._get_attrs(key)
        return (chars, attrs)

    def __setitem__(
        self,
        key: Union[int, tuple[int, ...]],
        value: Union[str, dict[str, str], tuple[str, dict[str, str]]],
    ) -> None:
        """Set character(s) and/or attribute(s) with type-based dispatch.

        Dispatches based on value type:
        - str: sets only characters
        - dict: sets only attributes
        - tuple: sets both (must be (str, dict))

        Examples:
            grid[0] = 'hello'                           # Chars only
            grid[0] = {'class': 'red'}                  # Attrs only
            grid[0] = ('hello', {'class': 'red'})       # Both
        """
        if isinstance(value, tuple):
            # Tuple: set both chars and attrs
            if len(value) != 2:
                raise ValueError("Tuple assignment requires exactly (text, attrs)")
            text, attrs = value
            if not isinstance(text, str):
                raise TypeError(f"First element must be str, got {type(text)}")
            if not isinstance(attrs, dict):
                raise TypeError(f"Second element must be dict, got {type(attrs)}")
            self._set_chars(key, text)
            self._set_attrs(key, attrs)
        elif isinstance(value, str):
            # String: set only chars
            self._set_chars(key, value)
        elif isinstance(value, dict):
            # Dict: set only attrs
            self._set_attrs(key, value)
        else:
            raise TypeError(
                f"Value must be str, dict, or tuple of (str, dict), got {type(value)}"
            )

    def _get_chars(self, key: Union[int, tuple[int, ...]]) -> Union[str, list[str]]:
        """Get character(s) from the grid."""
        if isinstance(key, int):
            # Single row index: grid[0] -> return row as string
            if 0 <= key < self.height:
                return "".join(self.chars[key])
            raise IndexError(f"Row index {key} out of range [0, {self.height})")

        if isinstance(key, tuple) and len(key) == 2:
            row_idx, col_idx = key

            # Both indices are integers: single cell
            if isinstance(row_idx, int) and isinstance(col_idx, int):
                if not (0 <= row_idx < self.height and 0 <= col_idx < self.width):
                    raise IndexError(f"Index ({row_idx}, {col_idx}) out of bounds")
                return self.chars[row_idx][col_idx]

            # Row is int, col is slice: grid[0, 2:5]
            if isinstance(row_idx, int) and isinstance(col_idx, slice):
                if not 0 <= row_idx < self.height:
                    raise IndexError(f"Row index {row_idx} out of range")
                cols = range(*col_idx.indices(self.width))
                return "".join(self.chars[row_idx][c] for c in cols)

            # Row is slice, col is int: column access
            if isinstance(row_idx, slice) and isinstance(col_idx, int):
                if not 0 <= col_idx < self.width:
                    raise IndexError(f"Column index {col_idx} out of range")
                rows = range(*row_idx.indices(self.height))
                return "".join(self.chars[r][col_idx] for r in rows)

            # Both are slices: 2D region
            if isinstance(row_idx, slice) and isinstance(col_idx, slice):
                rows = range(*row_idx.indices(self.height))
                cols = range(*col_idx.indices(self.width))
                return ["".join(self.chars[r][c] for c in cols) for r in rows]

        raise TypeError(f"Invalid index type: {type(key)}")

    def _get_attrs(
        self, key: Union[int, tuple[int, ...]]
    ) -> Union[dict[str, str], list[dict[str, str]], list[list[dict[str, str]]]]:
        """Get attribute(s) from the grid."""
        if isinstance(key, int):
            # Single row index: return list of attr dicts for the row
            if 0 <= key < self.height:
                return [attrs.copy() for attrs in self.attrs[key]]
            raise IndexError(f"Row index {key} out of range [0, {self.height})")

        if isinstance(key, tuple) and len(key) == 2:
            row_idx, col_idx = key

            # Both indices are integers: single cell
            if isinstance(row_idx, int) and isinstance(col_idx, int):
                if not (0 <= row_idx < self.height and 0 <= col_idx < self.width):
                    raise IndexError(f"Index ({row_idx}, {col_idx}) out of bounds")
                return self.attrs[row_idx][col_idx].copy()

            # Handle slices by returning lists
            if isinstance(row_idx, int) and isinstance(col_idx, slice):
                if not 0 <= row_idx < self.height:
                    raise IndexError(f"Row index {row_idx} out of range")
                cols = range(*col_idx.indices(self.width))
                return [self.attrs[row_idx][c].copy() for c in cols]

            if isinstance(row_idx, slice) and isinstance(col_idx, int):
                if not 0 <= col_idx < self.width:
                    raise IndexError(f"Column index {col_idx} out of range")
                rows = range(*row_idx.indices(self.height))
                return [self.attrs[r][col_idx].copy() for r in rows]

            if isinstance(row_idx, slice) and isinstance(col_idx, slice):
                rows = range(*row_idx.indices(self.height))
                cols = range(*col_idx.indices(self.width))
                return [[self.attrs[r][c].copy() for c in cols] for r in rows]

        raise TypeError(f"Invalid index type: {type(key)}")

    def _set_chars(self, key: Union[int, tuple[int, ...]], value: str) -> None:
        """Set character(s) with intelligent broadcasting."""
        if isinstance(key, int):
            # Single row index: grid[0] = 'hello'
            if not 0 <= key < self.height:
                raise IndexError(f"Row index {key} out of range [0, {self.height})")
            self._set_row_chars(key, value)
            return

        if isinstance(key, tuple) and len(key) == 2:
            row_idx, col_idx = key

            # Both indices are integers: single cell
            if isinstance(row_idx, int) and isinstance(col_idx, int):
                if not (0 <= row_idx < self.height and 0 <= col_idx < self.width):
                    raise IndexError(f"Index ({row_idx}, {col_idx}) out of bounds")
                # Only take first character
                self.chars[row_idx][col_idx] = value[0] if value else " "
                return

            # Get cells to update
            cells = self._get_cells_from_slice(row_idx, col_idx)
            self._broadcast_chars_to_cells(cells, value)
            return

        raise TypeError(f"Invalid index type: {type(key)}")

    def _set_attrs(
        self, key: Union[int, tuple[int, ...]], value: dict[str, str]
    ) -> None:
        """Set attribute(s) with intelligent broadcasting."""
        if isinstance(key, int):
            # Single row index: broadcast to entire row
            if not 0 <= key < self.height:
                raise IndexError(f"Row index {key} out of range [0, {self.height})")
            for col in range(self.width):
                self.attrs[key][col] = {**self.attrs[key][col], **value}
            return

        if isinstance(key, tuple) and len(key) == 2:
            row_idx, col_idx = key

            # Both indices are integers: single cell
            if isinstance(row_idx, int) and isinstance(col_idx, int):
                if not (0 <= row_idx < self.height and 0 <= col_idx < self.width):
                    raise IndexError(f"Index ({row_idx}, {col_idx}) out of bounds")
                self.attrs[row_idx][col_idx] = {
                    **self.attrs[row_idx][col_idx],
                    **value,
                }
                return

            # Get cells and broadcast attrs to all
            cells = self._get_cells_from_slice(row_idx, col_idx)
            for row, col in cells:
                self.attrs[row][col] = {**self.attrs[row][col], **value}
            return

        raise TypeError(f"Invalid index type: {type(key)}")

    def _set_row_chars(self, row: int, text: str) -> None:
        """Set an entire row with broadcasting.

        Broadcasting only occurs for single-character strings.
        Multi-character strings are written once without repeating.
        """
        if not text:
            text = self.fill_char

        # Single character: broadcast/repeat across all columns
        if len(text) == 1:
            for col in range(self.width):
                self.chars[row][col] = text[0]
        else:
            # Multi-character: write once, pad with fill_char if needed
            for col in range(self.width):
                self.chars[row][col] = text[col] if col < len(text) else self.fill_char

    def _broadcast_chars_to_cells(
        self, cells: list[tuple[int, int]], text: str
    ) -> None:
        """Broadcast text to a list of cells.

        Broadcasting only occurs for single-character strings.
        Multi-character strings are written once without repeating.
        """
        if not text:
            text = self.fill_char

        # Single character: broadcast/repeat across all cells
        if len(text) == 1:
            for row, col in cells:
                self.chars[row][col] = text[0]
        else:
            # Multi-character: write once, pad with fill_char if needed
            for i, (row, col) in enumerate(cells):
                self.chars[row][col] = text[i] if i < len(text) else self.fill_char

    def _get_cells_from_slice(
        self, row_idx: Union[int, slice], col_idx: Union[int, slice]
    ) -> list[tuple[int, int]]:
        """Convert row/col indices (potentially slices) to list of (row, col) tuples."""
        # Handle row index
        if isinstance(row_idx, int):
            if not 0 <= row_idx < self.height:
                raise IndexError(f"Row index {row_idx} out of range")
            rows = [row_idx]
        else:
            rows = list(range(*row_idx.indices(self.height)))

        # Handle col index
        if isinstance(col_idx, int):
            if not 0 <= col_idx < self.width:
                raise IndexError(f"Column index {col_idx} out of range")
            cols = [col_idx]
        else:
            cols = list(range(*col_idx.indices(self.width)))

        # Return cartesian product for 2D slices, or zip for 1D
        if isinstance(row_idx, slice) and isinstance(col_idx, slice):
            # 2D region: cartesian product
            return [(r, c) for r in rows for c in cols]
        else:
            # 1D slice: parallel assignment
            return [(r, c) for r in rows for c in cols]

    # ==================== Cursor and Print Methods ====================

    def _expand_if_needed(self, row: int, col: int) -> None:
        """Expand the grid if the given position is out of bounds.

        Args:
            row: Row index to check
            col: Column index to check
        """
        # Expand height if needed
        if row >= self.height:
            rows_to_add = row - self.height + 1
            for _ in range(rows_to_add):
                self.chars.append([self.fill_char] * self.width)
                self.attrs.append([{} for _ in range(self.width)])
            self.height = row + 1

        # Expand width if needed
        if col >= self.width:
            cols_to_add = col - self.width + 1
            for row_idx in range(self.height):
                self.chars[row_idx].extend([self.fill_char] * cols_to_add)
                self.attrs[row_idx].extend([{} for _ in range(cols_to_add)])
            self.width = col + 1

    def print(
        self,
        text: str = "",
        color: Optional[str] = None,
        bg_color: Optional[str] = None,
        bold: bool = False,
        dim: bool = False,
        underline: bool = False,
        endl: bool = True,
        **attrs: str,
    ) -> None:
        """Print text to the grid at the current cursor position.

        This method provides a convenient interface for writing styled text to the grid,
        similar to printing to a console. The grid will automatically expand if needed.

        Args:
            text: The text to print (supports newlines)
            color: Foreground color ('red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white', 'black')
            bg_color: Background color (same options as color)
            bold: Apply bold style
            dim: Apply dim style
            underline: Apply underline style
            endl: Whether to print a newline at the end of the text (default: True)
            **attrs: Additional HTML attributes to apply

        Examples:
            grid.print("Hello", color="red", bold=True)
            grid.print("World\\n", color="green")
            grid.print("Status: OK", color="cyan", bg_color="blue")
        """
        # Build the class string from style arguments
        classes = []
        if color:
            classes.append(f"ansi-{color}")
        if bg_color:
            classes.append(f"ansi-bg-{bg_color}")
        if bold:
            classes.append("ansi-bold")
        if dim:
            classes.append("ansi-dim")
        if underline:
            classes.append("ansi-underline")

        # Build attributes dict
        cell_attrs: dict[str, str] = {}
        if classes:
            cell_attrs["class"] = " ".join(classes)
        # Add any additional HTML attributes
        cell_attrs.update(attrs)

        # Process text character by character
        for char in text:
            if char == "\n":
                # Newline: move to start of next row
                self.cursor_row += 1
                self.cursor_col = 0
            else:
                # Expand grid if needed
                self._expand_if_needed(self.cursor_row, self.cursor_col)

                # Write character and attributes
                self.chars[self.cursor_row][self.cursor_col] = char
                if cell_attrs:
                    self.attrs[self.cursor_row][self.cursor_col] = {
                        **self.attrs[self.cursor_row][self.cursor_col],
                        **cell_attrs,
                    }

                # Advance cursor
                self.cursor_col += 1
        if endl:
            self.cursor_row += 1
            self.cursor_col = 0

    # ==================== Terminal Rendering Methods ====================

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
        codes = MonospaceGrid._parse_classes_to_ansi(attrs.get("class", ""))

        if not codes:
            return ""

        return f"\033[{';'.join(codes)}m"

    def _render_content_terminal(self) -> list[str]:
        """Render the grid content (without border) to terminal lines.

        Returns:
            List of rendered lines with ANSI escape codes
        """
        output: list[str] = []
        current_attrs: dict[str, str] = {}  # Tracks the currently applied attributes

        for y in range(self.height):
            line: list[str] = []

            # Start first line with a reset for safety
            if y == 0:
                line.append("\033[0m")

            for x in range(self.width):
                char = self.chars[y][x]
                attrs = self.attrs[y][x]

                if attrs != current_attrs:
                    # Attributes changed: reset and apply new code
                    line.append("\033[0m")
                    line.append(self._attrs_to_ansi_code(attrs))
                    current_attrs = attrs

                line.append(char)

            # End of row: reset and prepare for next row
            line.append("\033[0m")
            output.append("".join(line))
            # Reset tracking for next row
            current_attrs = {}

        return output

    def _add_border_terminal(self, content_lines: list[str]) -> str:
        """Add border around content lines for terminal output.

        Args:
            content_lines: List of rendered content lines

        Returns:
            Complete bordered output string
        """
        result: list[str] = []
        border_ansi = self._attrs_to_ansi_code(self.border_attrs)
        reset = "\033[0m"

        # Calculate dimensions
        content_width = self.width
        padding = self.border_padding
        inner_width = content_width + 2 * padding  # padding on both sides

        # Top border: ╭────╮
        result.append(f"{reset}{border_ansi}╭{'─' * inner_width}╮{reset}")

        # Top padding rows
        for _ in range(padding):
            result.append(f"{reset}{border_ansi}│{' ' * inner_width}│{reset}")

        # Content rows with side padding
        for line in content_lines:
            # Strip the reset code at the end of content line if present
            stripped_line = line.rstrip()
            if stripped_line.endswith("\033[0m"):
                stripped_line = stripped_line[:-4]

            result.append(
                f"{reset}{border_ansi}│{' ' * padding}{reset}"
                f"{stripped_line}"
                f"{reset}{border_ansi}{' ' * padding}│{reset}"
            )

        # Bottom padding rows
        for _ in range(padding):
            result.append(f"{reset}{border_ansi}│{' ' * inner_width}│{reset}")

        # Bottom border: ╰────╯
        result.append(f"{reset}{border_ansi}╰{'─' * inner_width}╯{reset}")

        return "\n".join(result)

    def to_console(self) -> str:
        """Render the grid to a terminal-friendly string with ANSI escape codes.

        Returns:
            String with ANSI escape codes for terminal output
        """
        # Render the core grid content
        content_lines = self._render_content_terminal()

        # If no border, return content as-is
        if not self.border:
            return "\n".join(content_lines)

        # Add border around content
        return self._add_border_terminal(content_lines)

    # ==================== HTML Rendering Methods ====================

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

    def _render_content_html(self) -> list[str]:
        """Render the grid content (without border) to HTML lines.

        Returns:
            List of rendered HTML lines
        """
        output: list[str] = []
        current_attrs: dict[str, str] = {}  # Tracks the currently applied attributes

        for y in range(self.height):
            line: list[str] = []
            for x in range(self.width):
                char = self.chars[y][x]
                attrs = self.attrs[y][x]

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
                        attrs_str = self._attrs_to_html_attrs(attrs)
                        line.append(f"<span {attrs_str}>")

                    current_attrs = attrs

                line.append(safe_char)

            # End of row: ensure any open span is closed
            if current_attrs:
                line.append("</span>")

            # Reset attrs tracking for the next line
            current_attrs = {}
            output.append("".join(line))

        return output

    def _add_border_html(self, content_lines: list[str]) -> list[str]:
        """Add border around content lines for HTML output.

        Args:
            content_lines: List of rendered content lines

        Returns:
            List of lines with border added
        """
        result: list[str] = []

        # Calculate dimensions
        content_width = self.width
        padding = self.border_padding
        inner_width = content_width + 2 * padding  # padding on both sides

        # Get border HTML attributes
        border_html_attrs = self._attrs_to_html_attrs(self.border_attrs)
        border_span_open = f"<span {border_html_attrs}>" if border_html_attrs else ""
        border_span_close = "</span>" if border_html_attrs else ""

        # Top border: ╭────╮
        result.append(f"{border_span_open}╭{'─' * inner_width}╮{border_span_close}")

        # Top padding rows
        for _ in range(padding):
            result.append(f"{border_span_open}│{' ' * inner_width}│{border_span_close}")

        # Content rows with side padding
        for line in content_lines:
            result.append(
                f"{border_span_open}│{' ' * padding}{border_span_close}"
                f"{line}"
                f"{border_span_open}{' ' * padding}│{border_span_close}"
            )

        # Bottom padding rows
        for _ in range(padding):
            result.append(f"{border_span_open}│{' ' * inner_width}│{border_span_close}")

        # Bottom border: ╰────╯
        result.append(f"{border_span_open}╰{'─' * inner_width}╯{border_span_close}")

        return result

    def to_html(self, default_bg: str = "#000000") -> str:
        """Render the grid to HTML with attributes merged on spans.

        Args:
            default_bg: Default background color for the <pre> wrapper

        Returns:
            HTML string with attributes on span elements
        """
        # Render the core grid content
        content_lines = self._render_content_html()

        # If border is enabled, add border around content
        if self.border:
            content_lines = self._add_border_html(content_lines)

        # Wrap everything in a <pre> tag for monospaced font and whitespace preservation
        content = "\n".join(content_lines)

        # Add basic retro CSS for the wrapper <pre> tag
        html_style = f"""
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1;
            background-color: {default_bg};
            color: #FFFFFF;
            padding: 10px;
            border: 2px solid #555;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
            white-space: pre;
            display: inline-block;
        """
        return f'<pre style="{html_style}">{content}</pre>'

    # ==================== String Representation ====================

    def __repr__(self) -> str:
        """Return terminal representation of the grid."""
        return self.to_console()

    def __str__(self) -> str:
        """Return terminal representation of the grid."""
        return self.to_console()
