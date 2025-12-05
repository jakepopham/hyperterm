"""Demo script showcasing hyperterm capabilities."""

from hyperterm import MonospaceGrid, TerminalRenderer, HTMLRenderer


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

    terminal_output = TerminalRenderer.render(grid)
    html_output = HTMLRenderer.render(grid)


    # Render to terminal
    print("=" * 50)
    print("Terminal Output (ANSI):")
    print("=" * 50)
    print(terminal_output)
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
    <p style="color: #aaa; font-family: monospace; font-size: 12px; margin-top: 20px;">
        Note: The "Click me!" text has HTMX attributes (hx-get, data-action) that only appear in HTML.
    </p>
</body>
</html>"""
        )
    print("\nHTML output saved to demo_output.html")


if __name__ == "__main__":
    main()
