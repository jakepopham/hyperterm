"""MonospaceGrid class for character grid manipulation with Pythonic slicing API."""

from typing import Any, Union


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

    Examples:
        # Create grid
        grid = MonospaceGrid(width=80, height=24)

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
        """Set an entire row with broadcasting."""
        if not text:
            text = self.fill_char
        for col in range(self.width):
            self.chars[row][col] = text[col % len(text)]

    def _broadcast_chars_to_cells(
        self, cells: list[tuple[int, int]], text: str
    ) -> None:
        """Broadcast text to a list of cells with cycling."""
        if not text:
            text = self.fill_char
        for i, (row, col) in enumerate(cells):
            self.chars[row][col] = text[i % len(text)]

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
