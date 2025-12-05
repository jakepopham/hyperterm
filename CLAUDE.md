# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hyperterm** is a unified text rendering library for terminal and web. It provides a monospace grid abstraction that can be rendered to both ANSI terminal output and HTML, enabling consistent styled text rendering across different output targets.

## Core Architecture

The project is built around a central grid abstraction with pluggable renderers:

### 1. Grid System (`MonospaceGrid`)
- **Location**: `hyperterm/grid.py`
- **Purpose**: Core data structure holding characters and their attributes in a 2D grid
- Coordinates are `(row, col)` where row is y-axis, col is x-axis, and `(0, 0)` is top-left
- Stores two parallel 2D arrays: `chars` for characters and `attrs` for attribute dictionaries
- **Pythonic slicing API with type-based dispatch**:
  - `grid[row, col] = 'text'` → sets characters only
  - `grid[row, col] = {'class': 'red'}` → sets attributes only
  - `grid[row, col] = ('text', {'class': 'red'})` → sets both
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

**TerminalRenderer** (`hyperterm/renderers/terminal.py`)
- Converts `MonospaceGrid` to ANSI escape code strings
- Maps privileged ANSI classes to ANSI escape sequences
- Optimizes output by tracking attribute changes and only emitting ANSI codes when classes differ
- Resets attributes at end of each row for safety

**HTMLRenderer** (`hyperterm/renderers/html.py`)
- Converts `MonospaceGrid` to HTML with CSS classes
- Uses `<span>` tags with class attributes for styled regions
- Wraps output in `<pre>` tag with retro terminal aesthetic
- HTML-escapes special characters (`&`, `<`, `>`)
- Passes through all HTML attributes (including HTMX attributes like `hx-get`)

### 4. Project Structure
- `hyperterm/grid.py`: Core MonospaceGrid class with Pythonic slicing API
- `hyperterm/renderers/`: Renderer implementations (terminal.py, html.py)
- `hyperterm/colors.py`: Color mapping dictionaries
- `hyperterm/types.py`: Type definitions and protocols
- `demo.py`: Demo showing the grid system and rendering capabilities
- `main.py`: Simple entry point stub
- `tests/`: Comprehensive test suite
- `pyproject.toml`: Python project configuration (requires Python >=3.9)

## Development Commands

### Running the Demo
```bash
uv run python demo.py
```
This demonstrates the grid system by creating a styled "SYSTEM STATUS" display and rendering it to both terminal (ANSI) and HTML.

### Running Tests
```bash
uv run pytest
```

### Type Checking
```bash
uv run pyright
```

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

```python
from hyperterm import MonospaceGrid, TerminalRenderer, HTMLRenderer

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
print(TerminalRenderer.render(grid))
html = HTMLRenderer.render(grid)
```
