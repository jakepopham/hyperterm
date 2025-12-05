"""Example demonstrating the border feature."""

from hyperterm import MonospaceGrid, TerminalRenderer, HTMLRenderer


def main():
    """Demonstrate border feature with different configurations."""

    # Example 1: Basic border with default padding
    print("Example 1: Basic border (default padding=1)")
    print("-" * 50)
    grid1 = MonospaceGrid(width=20, height=3, border=True)
    grid1[1, 5:15] = ("Hello!", {"class": "ansi-green ansi-bold"})
    print(TerminalRenderer.render(grid1))
    print()

    # Example 2: Border with custom padding
    print("Example 2: Border with padding=2")
    print("-" * 50)
    grid2 = MonospaceGrid(width=20, height=3, border=True, border_padding=2)
    grid2[1, 5:15] = ("Padded!", {"class": "ansi-yellow"})
    print(TerminalRenderer.render(grid2))
    print()

    # Example 3: Border with custom styling
    print("Example 3: Styled border")
    print("-" * 50)
    grid3 = MonospaceGrid(
        width=25,
        height=4,
        border=True,
        border_padding=1,
        border_attrs={"class": "ansi-cyan ansi-bold"},
    )
    grid3[0] = ("═" * 25, {"class": "ansi-yellow ansi-bold"})
    grid3[1] = ("  Styled Border Demo  ", {"class": "ansi-white"})
    grid3[2] = ("═" * 25, {"class": "ansi-yellow ansi-bold"})
    print(TerminalRenderer.render(grid3))
    print()

    # Example 4: No border (comparison)
    print("Example 4: Same grid without border")
    print("-" * 50)
    grid4 = MonospaceGrid(width=20, height=3)
    grid4[1, 5:15] = ("No border", {"class": "ansi-red"})
    print(TerminalRenderer.render(grid4))
    print()

    # Example 5: Zero padding
    print("Example 5: Border with zero padding")
    print("-" * 50)
    grid5 = MonospaceGrid(width=15, height=2, border=True, border_padding=0)
    grid5[0, 2:13] = ("Tight fit", {"class": "ansi-magenta"})
    print(TerminalRenderer.render(grid5))
    print()

    print("Note: The border is added outside the indexable grid area.")
    print("grid[0, 0] still refers to the first content cell, not the border.")


if __name__ == "__main__":
    main()
