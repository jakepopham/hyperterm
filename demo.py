"""Demo script showcasing hyperterm capabilities."""

from hyperterm import MonospaceGrid


def main():
    """Demonstrate hyperterm by creating a styled terminal interface."""
    # Create a 40x12 grid
    grid = MonospaceGrid(width=40, height=12, fill_char=".")

    # Draw a colored border box (yellow, bold) using type-based dispatch
    # Top and bottom borders (combined char + attrs)
    grid[2, 5:35] = ("█" * 30, {"class": "ansi-yellow ansi-bold"})
    grid[9, 5:35] = ("█" * 30, {"class": "ansi-yellow ansi-bold"})
    # Left and right borders (also combined)
    grid[3:9, 5] = ("█", {"class": "ansi-yellow ansi-bold"})
    grid[3:9, 34] = ("█", {"class": "ansi-yellow ansi-bold"})

    # Draw a title in the center (bold, red)
    title = "SYSTEM STATUS"
    x_title = 20 - len(title) // 2
    grid[3, x_title : x_title + len(title)] = (title, {"class": "ansi-red ansi-bold"})

    # Draw a line of normal text (white)
    grid[5, 7:25] = ("Loading modules...", {"class": "ansi-white"})

    # Draw a highlighted sequence (cyan text)
    grid[7, 7:25] = ("Module BIND_34... ", {"class": "ansi-cyan"})

    # Draw status indicator (green on blue, underlined)
    grid[7, 25:29] = ("[OK]", {"class": "ansi-green ansi-bg-blue ansi-underline"})

    # Draw an error message (yellow text on red background, bold)
    error = "ERROR: MEMORY ACCESS DENIED"
    x_error = 20 - len(error) // 2
    grid[9, x_error : x_error + len(error)] = (
        error,
        {"class": "ansi-yellow ansi-bg-red ansi-bold"},
    )

    # Demonstrate custom HTMX attributes (only visible in HTML)
    grid[11, 7:16] = (
        "Click me!",
        {"class": "ansi-cyan clickable", "hx-get": "/data", "data-action": "test"},
    )

    terminal_output = grid.to_console()
    html_output = grid.to_html()

    # Create a second grid with border feature enabled and title
    bordered_grid = MonospaceGrid(
        width=30,
        height=5,
        fill_char=" ",
        border=True,
        border_padding=1,
        border_attrs={"class": "ansi-cyan ansi-bold"},
        title="BORDER DEMO",
    )

    # Add some content to the bordered grid
    text1 = "Automatic box borders!"
    bordered_grid[1, 4:4+len(text1)] = (text1, {"class": "ansi-green"})

    text2 = "With configurable padding"
    bordered_grid[2, 3:3+len(text2)] = (text2, {"class": "ansi-white"})

    text3 = "And title headers!"
    bordered_grid[3, 5:5+len(text3)] = (text3, {"class": "ansi-yellow"})

    bordered_terminal = bordered_grid.to_console()
    bordered_html = bordered_grid.to_html()

    # Create a third grid demonstrating the new print() method with auto-expanding
    print_demo_grid = MonospaceGrid(border=True, title="System Status")
    print_demo_grid.print("Welcome to ", color="cyan", bold=True)
    print_demo_grid.print("hyperterm", color="yellow", bold=True, underline=True)
    print_demo_grid.print("!\n", color="cyan", bold=True)
    print_demo_grid.print("\n")
    print_demo_grid.print("Status: ", color="white")
    print_demo_grid.print("ONLINE", color="green", bg_color="black", bold=True)
    print_demo_grid.print("\n")
    print_demo_grid.print("CPU: ", color="white")
    print_demo_grid.print("OK", color="green", bold=True)
    print_demo_grid.print("  Memory: ", color="white")
    print_demo_grid.print("OK", color="green", bold=True)
    print_demo_grid.print("\n")
    print_demo_grid.print("Disk: ", color="white")
    print_demo_grid.print("WARNING", color="yellow", bold=True)

    print_demo_terminal = print_demo_grid.to_console()
    print_demo_html = print_demo_grid.to_html()

    # Render to terminal
    print("=" * 50)
    print("Terminal Output (ANSI):")
    print("=" * 50)
    print(terminal_output)
    print("=" * 50)
    print()
    print("=" * 50)
    print("Terminal Output with Border:")
    print("=" * 50)
    print(bordered_terminal)
    print("=" * 50)
    print()
    print("=" * 50)
    print("New print() Method Demo (Auto-expanding):")
    print("=" * 50)
    print(print_demo_terminal)
    print("=" * 50)
    print(f"Grid auto-expanded to: {print_demo_grid.width}x{print_demo_grid.height}")
    print(f"Cursor position: ({print_demo_grid.cursor_row}, {print_demo_grid.cursor_col})")
    print("=" * 50)
    print()

    # Save HTML to file with CSS styles for privileged classes
    with open("demo_output.html", "w") as f:
        f.write(
            f"""<!DOCTYPE html>
<html>
<head>
    <title>Hyperterm Demo</title>
    <meta charset="utf-8">
    <style>
        /* Privileged ANSI foreground color classes */
        .ansi-black {{ color: #000000; }}
        .ansi-red {{ color: #FF4444; }}
        .ansi-green {{ color: #44FF44; }}
        .ansi-yellow {{ color: #FFFF44; }}
        .ansi-blue {{ color: #4444FF; }}
        .ansi-magenta {{ color: #FF44FF; }}
        .ansi-cyan {{ color: #44FFFF; }}
        .ansi-white {{ color: #FFFFFF; }}

        /* Privileged ANSI background color classes */
        .ansi-bg-black {{ background-color: #000000; }}
        .ansi-bg-red {{ background-color: #AA0000; }}
        .ansi-bg-green {{ background-color: #00AA00; }}
        .ansi-bg-yellow {{ background-color: #AAAA00; }}
        .ansi-bg-blue {{ background-color: #0000AA; }}
        .ansi-bg-magenta {{ background-color: #AA00AA; }}
        .ansi-bg-cyan {{ background-color: #00AAAA; }}
        .ansi-bg-white {{ background-color: #888888; }}

        /* Privileged ANSI text style classes */
        .ansi-bold {{ font-weight: bold; }}
        .ansi-dim {{ opacity: 0.5; }}
        .ansi-underline {{ text-decoration: underline; }}

        /* Custom classes (non-privileged) */
        .clickable {{
            cursor: pointer;
            transition: opacity 0.2s;
        }}
        .clickable:hover {{
            opacity: 0.8;
            text-decoration: underline;
        }}
    </style>
</head>
<body style="background-color: #1a1a1a; padding: 20px;">
    <h1 style="color: white; font-family: monospace;">Hyperterm Demo</h1>
    <p style="color: #aaa; font-family: monospace; font-size: 14px;">
        This demonstrates interoperability between terminal and web rendering.<br>
        The same privileged classes (ansi-*) work in both contexts:<br>
        • Terminal: Converted to ANSI escape codes<br>
        • Web: Styled via CSS classes
    </p>
    {html_output}
    <h2 style="color: white; font-family: monospace; margin-top: 30px;">Border Feature Demo</h2>
    <p style="color: #aaa; font-family: monospace; font-size: 14px;">
        The border is added outside the normal indexable grid area.<br>
        Grid dimensions remain unchanged - border and padding are added at render time.
    </p>
    {bordered_html}
    <h2 style="color: white; font-family: monospace; margin-top: 30px;">New print() Method Demo</h2>
    <p style="color: #aaa; font-family: monospace; font-size: 14px;">
        Using the new print() method with auto-expanding grid.<br>
        Grid started at 0x0 and expanded to {print_demo_grid.width}x{print_demo_grid.height} automatically!<br>
        Convenient styling with color, bold, underline parameters.
    </p>
    {print_demo_html}
    <p style="color: #aaa; font-family: monospace; font-size: 12px; margin-top: 20px;">
        Note: The "Click me!" text has HTMX attributes (hx-get, data-action) that only appear in HTML.
    </p>
</body>
</html>"""
        )
    print("\nHTML output saved to demo_output.html")


if __name__ == "__main__":
    main()
