# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

**hyperterm** is a unified text rendering library for terminal and web. It provides a monospace grid abstraction that can be rendered to both ANSI terminal output and HTML, enabling consistent styled text rendering across different output targets.

The core value proposition: write styled text once, render it anywhere.

## Core Architecture

The project is built around a central grid abstraction with pluggable renderers:

### 1. Grid System (`MonospaceGrid`)
- **Location**: `hyperterm/grid.py`
- **Purpose**: Core data structure holding characters and their attributes in a 2D grid
- Coordinates are `(row, col)` where row is y-axis, col is x-axis, and `(0, 0)` is top-left
- Stores two parallel 2D arrays: `chars` for characters and `attrs` for attribute dictionaries
- **Pythonic slicing API with type-based dispatch**:
  - `grid[row, col] = 'text'` sets characters only
  - `grid[row, col] = {'class': 'red'}` sets attributes only
  - `grid[row, col] = ('text', {'class': 'red'})` sets both
  - Supports full Python slicing: `grid[0:5, 10:20]`, `grid[:, 0]`, etc.
  - Intelligent broadcasting: short strings cycle across longer slices

### 2. Attribute System
- **Location**: `hyperterm/grid.py` (attrs field)
- Each grid cell has an associated `dict[str, str]` for HTML attributes
- Supports privileged ANSI classes (e.g., 'ansi-red', 'ansi-bold', 'ansi-bg-blue')
- Also supports custom HTML attributes (e.g., 'hx-get', 'data-action')
- **Privileged ANSI classes**:
  - Colors: 'ansi-red', 'ansi-green', 'ansi-blue', 'ansi-yellow', 'ansi-cyan', 'ansi-magenta', 'ansi-white', 'ansi-black'
  - Background: 'ansi-bg-red', 'ansi-bg-green', etc.
  - Styles: 'ansi-bold', 'ansi-dim', 'ansi-underline'

### 3. Renderer Pattern
The library uses separate renderer classes for different output targets:

**Terminal Renderer** (grid methods: `to_console()`)
- **Location**: `hyperterm/grid.py` (methods: `_render_content_terminal`, `_add_border_terminal`, `to_console`)
- Converts `MonospaceGrid` to ANSI escape code strings
- Maps privileged ANSI classes to ANSI escape sequences
- Optimizes output by tracking attribute changes and only emitting ANSI codes when classes differ
- Resets attributes at end of each row for safety

**HTML Renderer** (grid methods: `to_html()`)
- **Location**: `hyperterm/grid.py` (methods: `_render_content_html`, `_add_border_html`, `to_html`)
- Converts `MonospaceGrid` to HTML with CSS classes
- Uses `<span>` tags with class attributes for styled regions
- Wraps output in `<pre>` tag with retro terminal aesthetic
- HTML-escapes special characters (`&`, `<`, `>`)
- Passes through all HTML attributes (including HTMX attributes like `hx-get`)

### 4. Project Structure
```
hyperterm/
├── __init__.py           # Package exports
├── grid.py               # Core MonospaceGrid class with rendering methods
├── colors.py             # ANSI color mapping dictionaries
├── types.py              # Type definitions and protocols
└── style.py              # (Unused) Style utilities
tests/
├── test_grid.py          # Core grid functionality tests
├── test_border.py        # Border and title feature tests
├── test_title.py         # Title-specific tests
├── test_terminal_renderer.py  # Terminal rendering tests
├── test_html_renderer.py      # HTML rendering tests
├── test_integration.py        # End-to-end integration tests
└── test_colors.py             # Color mapping tests
demo.py                   # Comprehensive demonstration script
pyproject.toml            # Python project configuration (requires Python >=3.9)
```

## Development Commands

### Running the Demo
```bash
uv run python demo.py
```
This demonstrates the grid system by creating multiple styled displays and rendering them to both terminal (ANSI) and HTML. It generates a `demo_output.html` file that can be opened in a browser.

### Running Tests
```bash
uv run pytest
```
Run tests with coverage:
```bash
uv run pytest --cov
```

### Type Checking
```bash
uv run pyright
```

The codebase should have zero pyright errors. Type annotations are comprehensive and include support for the slicing API.

## Key Design Patterns

1. **Separation of Concerns**: The grid abstraction is completely independent of rendering. Renderers operate on the grid without modifying it.

2. **Type-Based Dispatch**: The grid indexing API uses intelligent type dispatch:
   - String values set characters
   - Dict values set attributes
   - Tuple values set both
   This eliminates the need for separate methods like `draw_text()` and `draw_box()`.

3. **Intelligent Broadcasting**: Short strings automatically cycle across longer slices, making it easy to fill borders or patterns.

4. **Attribute State Tracking**: Both renderers track the "current" attribute set and only emit changes when necessary, optimizing output size.

5. **Dual Output Strategy**: Attributes are stored in a renderer-agnostic way, with privileged ANSI classes that map to both ANSI escape codes and CSS classes.

## API Examples

### Basic Usage
```python
from hyperterm import MonospaceGrid

# Create grid
grid = MonospaceGrid(width=80, height=24)

# Set characters only
grid[0] = 'Hello World'              # Full row with broadcasting
grid[1, 5] = 'X'                     # Single character
grid[2, 10:20] = 'status'            # Slice with cycling

# Set attributes only
grid[0] = {'class': 'ansi-red'}      # Style entire row
grid[1, 5:10] = {'class': 'ansi-bold'}  # Style slice

# Set both at once
grid[3, :10] = ('TITLE', {'class': 'ansi-yellow ansi-bold'})

# Vertical borders using column slicing
grid[:, 0] = ('|', {'class': 'ansi-cyan'})

# Render
print(grid.to_console())
html = grid.to_html()
```

### Auto-Expanding Grids with Print Interface
```python
from hyperterm import MonospaceGrid

# Grid starts at 0x0 and expands automatically
grid = MonospaceGrid(border=True, title='Log Output')

grid.print('Status: ', color='white')
grid.print('OK', color='green', bold=True)
grid.print('\n')
grid.print('CPU: 45%', color='yellow')

# Grid has automatically expanded to fit content
print(f"Grid size: {grid.width}x{grid.height}")
print(grid.to_console())
```

### Borders and Titles
```python
from hyperterm import MonospaceGrid

grid = MonospaceGrid(
    width=40,
    height=10,
    border=True,
    border_padding=2,
    border_attrs={'class': 'ansi-cyan ansi-bold'},
    title='Dashboard'
)

# Content is indexed normally - border is added at render time
grid[0, 5:15] = ('Welcome!', {'class': 'ansi-green'})

print(grid.to_console())
```

## Type System

The codebase uses comprehensive type annotations:

- **Slicing support**: `Union[int, tuple[Union[int, slice], Union[int, slice]]]`
- **Value types**: `Union[str, dict[str, str], tuple[str, dict[str, str]]]`
- **Return types**: Properly annotated to include all possible return values including nested lists

Some type ignores are present for:
- Defensive isinstance checks that are technically redundant but good practice
- Test cases that intentionally use invalid types to test error handling
- Access to protected methods in tests

## Testing Philosophy

- **Comprehensive coverage**: 114 tests covering all major features
- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test complete workflows (create, draw, render)
- **Both renderers**: Most features tested in both terminal and HTML contexts
- **Edge cases**: Tests for boundary conditions, empty grids, invalid inputs

## Common Patterns

### Drawing Boxes
```python
# Horizontal lines
grid[0, :] = ('─', {'class': 'ansi-cyan'})
grid[9, :] = ('─', {'class': 'ansi-cyan'})

# Vertical lines
grid[:, 0] = ('│', {'class': 'ansi-cyan'})
grid[:, 19] = ('│', {'class': 'ansi-cyan'})

# Corners
grid[0, 0] = ('┌', {'class': 'ansi-cyan'})
grid[0, 19] = ('┐', {'class': 'ansi-cyan'})
grid[9, 0] = ('└', {'class': 'ansi-cyan'})
grid[9, 19] = ('┘', {'class': 'ansi-cyan'})
```

### Status Indicators
```python
# Traffic light pattern
grid[1, 5:10] = ('OK', {'class': 'ansi-green ansi-bold'})
grid[2, 5:13] = ('WARNING', {'class': 'ansi-yellow ansi-bold'})
grid[3, 5:11] = ('ERROR', {'class': 'ansi-red ansi-bold'})
```

### Progress Bars
```python
# Progress bar
total = 20
progress = 12
grid[5, 10:10+progress] = ('█', {'class': 'ansi-green'})
grid[5, 10+progress:10+total] = ('░', {'class': 'ansi-dim'})
```

## Implementation Notes

### Grid Indexing
- The `__getitem__` and `__setitem__` methods handle all indexing operations
- Helper methods `_get_chars`, `_get_attrs`, `_set_chars`, `_set_attrs` do the actual work
- Type narrowing determines whether we're dealing with single cells, rows, columns, or 2D regions

### Broadcasting Logic
- Single-character strings repeat across the target region
- Multi-character strings write once and pad with fill_char if needed
- This makes it easy to draw borders: `grid[:, 0] = '|'`

### Attribute Merging
- When setting attributes, they merge with existing attributes using dict spread: `{**existing, **new}`
- This allows incremental styling without losing previous attributes

### Border Implementation
- Borders are added at render time, not stored in the grid
- Grid dimensions refer to the content area only
- Border calculations account for padding on all sides
- Title is rendered inline in the top border

### Rendering Optimization
- Both renderers track "current" attributes to minimize output
- Terminal renderer only emits ANSI codes when attributes change
- HTML renderer groups adjacent cells with same attributes into single spans

## When Making Changes

1. **Type Safety**: Ensure all new code has proper type annotations and passes pyright
2. **Test Coverage**: Add tests for new features in appropriate test files
3. **Both Renderers**: Consider how changes affect both terminal and HTML output
4. **Backwards Compatibility**: The slicing API is core - don't break existing patterns
5. **Documentation**: Update examples in README.md and CLAUDE.md

## Performance Considerations

- Grid operations are O(n) where n is the number of cells affected
- Broadcasting is efficient for single characters (no string operations)
- Rendering is O(width * height) but with optimizations to skip unchanged attributes
- Large grids (1000x1000) render in milliseconds

## Future Extension Points

The architecture supports easy extension:

1. **New Renderers**: Add new output formats by implementing the renderer pattern
2. **Custom Attributes**: Any HTML attribute passes through (already supported)
3. **Rich Text**: Could add markdown-style parsing to the print() method
4. **Animations**: Could add frame sequencing for terminal animations
5. **Input Handling**: Could add input regions with HTMX for web forms
