"""MonospaceGrid class for character grid manipulation."""


class MonospaceGrid:
    """A grid structure for holding characters and their attributes.

    Coordinates are (x, y) where x is column and y is row.
    (0, 0) is top-left.

    Each cell has:
    - A character (str)
    - Attributes (dict[str, str]) for HTML/styling purposes

    Attributes:
        width: Number of columns in the grid
        height: Number of rows in the grid
        fill_char: Character used to fill empty cells
        chars: 2D array of characters
        attrs: 2D array of attributes corresponding to each character
    """

    def __init__(self, width: int, height: int, fill_char: str = " ") -> None:
        """Initialize a new MonospaceGrid.

        Args:
            width: Number of columns
            height: Number of rows
            fill_char: Character to fill the grid with (default: space)
        """
        self.width: int = width
        self.height: int = height
        self.fill_char: str = fill_char

        # Initialize the grid with fill_char and empty attributes
        self.chars: list[list[str]] = [[fill_char] * width for _ in range(height)]
        self.attrs: list[list[dict[str, str]]] = [
            [{} for _ in range(width)] for _ in range(height)
        ]

    def _is_valid_coord(self, x: int, y: int) -> bool:
        """Helper to validate coordinates.

        Args:
            x: Column coordinate
            y: Row coordinate

        Returns:
            True if coordinate is within grid bounds
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def set_char(self, x: int, y: int, char: str) -> None:
        """Set a single character at (x, y).

        Args:
            x: Column coordinate
            y: Row coordinate
            char: Character to set (only first character is used)
        """
        if self._is_valid_coord(x, y):
            self.chars[y][x] = str(char)[0]  # Only take the first character
        else:
            print(f"Warning: Coordinate ({x}, {y}) out of bounds.")

    def set_attrs(self, x: int, y: int, attrs: dict[str, str]) -> None:
        """Set attributes for a single character at (x, y).

        Args:
            x: Column coordinate
            y: Row coordinate
            attrs: Dictionary of HTML attributes to set/merge
        """
        if self._is_valid_coord(x, y):
            # Merge new attributes with existing ones
            self.attrs[y][x] = {**self.attrs[y][x], **attrs}
        else:
            print(f"Warning: Coordinate ({x}, {y}) out of bounds.")

    def draw_text(
        self, x_start: int, y_start: int, text: str, attrs: dict[str, str] | None = None
    ) -> None:
        """Draw a string of text starting at (x_start, y_start) with optional attributes.

        Args:
            x_start: Starting column coordinate
            y_start: Starting row coordinate
            text: Text string to draw
            attrs: Dictionary of HTML attributes to apply to each character
        """
        attrs = attrs or {}
        for i, char in enumerate(text):
            x = x_start + i
            y = y_start
            if self._is_valid_coord(x, y):
                self.set_char(x, y, char)
                if attrs:
                    self.set_attrs(x, y, attrs)

    def draw_box(
        self, x: int, y: int, w: int, h: int, char: str = "#", attrs: dict[str, str] | None = None
    ) -> None:
        """Draw a simple rectangle outline.

        Args:
            x: Starting column coordinate (top-left)
            y: Starting row coordinate (top-left)
            w: Width of the box
            h: Height of the box
            char: Character to use for the box border (default: #)
            attrs: Dictionary of HTML attributes to apply to the border
        """
        attrs = attrs or {}
        for row in range(y, y + h):
            for col in range(x, x + w):
                # Check bounds for drawing
                if not self._is_valid_coord(col, row):
                    continue

                is_border = (
                    row == y or row == y + h - 1 or col == x or col == x + w - 1
                )

                if is_border:
                    self.set_char(col, row, char)
                    if attrs:
                        self.set_attrs(col, row, attrs)
