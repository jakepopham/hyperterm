# hyperterm

A unified text rendering library for terminal and web. Write styled text once, render it anywhere.

## Overview

hyperterm provides a monospace grid abstraction that can be rendered to both ANSI terminal output and HTML. This enables you to create rich, styled terminal interfaces and web displays from the same codebase, with consistent styling across both targets.

## Key Features

- **Dual Output**: Render the same grid to both terminal (with ANSI escape codes) and HTML (with CSS classes)
- **Pythonic Slicing API**: Intuitive indexing and slicing syntax for grid manipulation
- **Type-Based Dispatch**: Set characters, attributes, or both with intelligent type detection
- **Privileged ANSI Classes**: Special CSS classes that automatically convert to ANSI codes for terminal output
- **Automatic Borders**: Optional borders and titles with configurable padding and styling
- **Auto-Expanding Grids**: Print-like interface with automatic grid expansion
- **HTMX Support**: Pass-through of custom HTML attributes for interactive web interfaces

## Installation

```bash
pip install hyperterm
```

## Quick Start

```python
from hyperterm import MonospaceGrid

# Create a grid
grid = MonospaceGrid(width=40, height=10)

# Set characters only
grid[0] = 'Hello World'

# Set attributes only (applies styling)
grid[0] = {'class': 'ansi-red ansi-bold'}

# Set both at once
grid[1] = ('Status: OK', {'class': 'ansi-green'})

# Render to terminal
print(grid.to_console())

# Render to HTML
html = grid.to_html()
```

## Core Concepts

### The Grid

The `MonospaceGrid` is a 2D grid where each cell contains:
- A character (str)
- Attributes (dict[str, str]) for styling

Coordinates are `(row, col)` where `(0, 0)` is the top-left corner.

### Pythonic Slicing

The grid supports full Python slicing syntax:

```python
grid[0]              # Entire row
grid[0, 5]           # Single cell at row 0, column 5
grid[0, 5:10]        # Columns 5-9 of row 0
grid[:, 0]           # Entire column 0 (vertical)
grid[2:5, 10:20]     # 2D region
```

### Type-Based Dispatch

The grid intelligently handles different value types:

```python
# String: sets characters only
grid[0] = 'text'

# Dict: sets attributes only
grid[0] = {'class': 'ansi-red'}

# Tuple: sets both
grid[0] = ('text', {'class': 'ansi-red'})
```

### Privileged ANSI Classes

Special CSS classes that work in both terminal and HTML:

**Foreground Colors:**
- `ansi-black`, `ansi-red`, `ansi-green`, `ansi-yellow`
- `ansi-blue`, `ansi-magenta`, `ansi-cyan`, `ansi-white`

**Background Colors:**
- `ansi-bg-black`, `ansi-bg-red`, `ansi-bg-green`, `ansi-bg-yellow`
- `ansi-bg-blue`, `ansi-bg-magenta`, `ansi-bg-cyan`, `ansi-bg-white`

**Text Styles:**
- `ansi-bold`, `ansi-dim`, `ansi-underline`

These classes automatically convert to ANSI escape codes for terminal output and remain as CSS classes for HTML output.

## Examples

### Basic Styled Text

```python
from hyperterm import MonospaceGrid

grid = MonospaceGrid(width=30, height=3)

# Title in bold red
grid[0, 5:17] = ('SYSTEM ALERT', {'class': 'ansi-red ansi-bold'})

# Status message in green
grid[1, 5:20] = ('Status: Online', {'class': 'ansi-green'})

# Warning in yellow on red background
grid[2, 5:25] = ('Warning: Low Memory', {'class': 'ansi-yellow ansi-bg-red'})

print(grid.to_console())
```

### Borders and Titles

```python
from hyperterm import MonospaceGrid

grid = MonospaceGrid(
    width=30,
    height=5,
    border=True,
    border_padding=1,
    border_attrs={'class': 'ansi-cyan ansi-bold'},
    title='Status Panel'
)

grid[1, 5:20] = ('System: OK', {'class': 'ansi-green'})
grid[2, 5:20] = ('CPU: 45%', {'class': 'ansi-yellow'})
grid[3, 5:20] = ('Memory: 80%', {'class': 'ansi-red'})

print(grid.to_console())
```

### Print-Style Interface

```python
from hyperterm import MonospaceGrid

# Create an auto-expanding grid
grid = MonospaceGrid(border=True, title='Log Output')

# Print with styling
grid.print('Welcome to ', color='white')
grid.print('hyperterm', color='cyan', bold=True, underline=True)
grid.print('!\n', color='white')
grid.print('\n')
grid.print('Status: ', color='white')
grid.print('ONLINE', color='green', bg_color='black', bold=True)

print(grid.to_console())
```

### HTML with Custom Attributes

```python
from hyperterm import MonospaceGrid

grid = MonospaceGrid(width=20, height=3)

# Add HTMX attributes for interactive elements
grid[1, 2:15] = (
    'Click me!',
    {
        'class': 'ansi-cyan clickable',
        'hx-get': '/api/data',
        'hx-target': '#result',
        'data-action': 'fetch'
    }
)

html = grid.to_html()
# HTMX attributes pass through to HTML but are ignored in terminal rendering
```

### Vertical and Horizontal Lines

```python
from hyperterm import MonospaceGrid

grid = MonospaceGrid(width=20, height=10, fill_char=' ')

# Vertical borders using column slicing
grid[:, 0] = ('|', {'class': 'ansi-cyan'})
grid[:, 19] = ('|', {'class': 'ansi-cyan'})

# Horizontal borders using row slicing
grid[0, :] = ('-', {'class': 'ansi-cyan'})
grid[9, :] = ('-', {'class': 'ansi-cyan'})

# Content
grid[5, 5:15] = ('Centered', {'class': 'ansi-white'})

print(grid.to_console())
```

## API Reference

### MonospaceGrid

```python
MonospaceGrid(
    width: Optional[int] = None,
    height: Optional[int] = None,
    fill_char: str = " ",
    border: bool = True,
    border_padding: int = 1,
    border_attrs: Optional[dict[str, str]] = None,
    title: str = ""
)
```

**Parameters:**
- `width`: Number of columns (None for auto-expanding)
- `height`: Number of rows (None for auto-expanding)
- `fill_char`: Character to fill empty cells
- `border`: Whether to render a border around the grid
- `border_padding`: Space between border and content
- `border_attrs`: HTML attributes for border styling
- `title`: Title text displayed in top border

**Methods:**

- `grid[key]`: Get characters and attributes
- `grid[key] = value`: Set characters and/or attributes
- `to_console() -> str`: Render to ANSI terminal output
- `to_html(default_bg: str = "#000000") -> str`: Render to HTML
- `print(text, color, bg_color, bold, dim, underline, endl, **attrs)`: Print text with styling

## Rendering

### Terminal Rendering

The terminal renderer converts the grid to ANSI escape codes:
- Privileged ANSI classes become escape sequences
- Attributes are tracked and only changed when needed
- Each row ends with a reset for safety
- Borders are drawn with box-drawing characters

### HTML Rendering

The HTML renderer converts the grid to styled HTML:
- Characters are HTML-escaped
- All attributes pass through as HTML attributes
- Privileged ANSI classes remain as CSS classes
- Adjacent cells with identical attributes are grouped in spans
- Output is wrapped in a styled `<pre>` tag

## Architecture

hyperterm uses a clean separation of concerns:

1. **Grid Layer**: `MonospaceGrid` stores characters and attributes
2. **Renderer Layer**: Separate renderers convert grids to output formats
3. **Attribute System**: Unified attribute dictionary supports both targets

The grid is renderer-agnostic. Renderers read from the grid without modifying it, making it easy to render the same grid to multiple targets.

## Use Cases

- Terminal UI frameworks
- CLI dashboards and status displays
- Web-based terminal emulators
- Documentation with code examples that work in both contexts
- Debugging visualizations that work locally and in web interfaces
- HTMX-powered terminal-style web applications

## Requirements

- Python >= 3.9

## Testing

```bash
pytest
```

## License

MIT
