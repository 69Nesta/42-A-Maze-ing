"""Color schemes and color identifiers for the maze display.

This module defines a small `MazeColors` Enum used as keys for
color dictionaries and `MazeSchemesColors`, a container holding a list
of predefined color schemes and convenience accessors.
"""

from enum import Enum


class MazeColors(Enum):
    BACKGROUND = 0
    WALL = 1
    PATH = 2
    START = 3
    END = 4
    LOGO = 5


class MazeSchemesColors:
    def __init__(self) -> None:
        """Container for multiple color schemes and access helpers.

        Attributes:
            schemes: List of color mapping dictionaries keyed by
                `MazeColors` values.
            current_scheme: Index of the currently active color scheme.
            total_schemes: Cached number of available schemes.
        """

        self.schemes: list[dict[MazeColors, int]] = [
            # Original scheme purple-ish
            {
                MazeColors.BACKGROUND: 0xFFD9DBF1,
                MazeColors.WALL: 0xFF7D84B2,
                MazeColors.PATH: 0xFFF5B027,
                MazeColors.START: 0xFFDBF4A7,
                MazeColors.END: 0xFF8E9DCC,
                MazeColors.LOGO: 0xFFF9F9ED
            },

            # fff275, ff8c42, ff3c38, a23e48, 6c8ead Warm
            {
                MazeColors.BACKGROUND: 0xFFFFF275,
                MazeColors.WALL: 0xFFFF8C42,
                MazeColors.PATH: 0xFFFF3C38,
                MazeColors.START: 0xFFA23E48,
                MazeColors.END: 0xFF6C8EAD,
                MazeColors.LOGO: 0xFFD36582
            },

            # 88ccf1, c1dff0, 3587a4, 2d848a, 2d898b Blueish
            {
                MazeColors.BACKGROUND: 0xFF88CCF1,
                MazeColors.WALL: 0xFFC1DFF0,
                MazeColors.PATH: 0xFF3587A4,
                MazeColors.START: 0xFFC9A690,
                MazeColors.END: 0xFF637074,
                MazeColors.LOGO: 0xFFBDD4E7,
            },

            # 242331, 533e2d, a27035, b88b4a, ddca7d Earthy
            {
                MazeColors.BACKGROUND: 0xFF242331,
                MazeColors.WALL: 0xFF533E2D,
                MazeColors.PATH: 0xFFA27035,
                MazeColors.START: 0xFFB88B4A,
                MazeColors.END: 0xFFDDCA7D,
                MazeColors.LOGO: 0xFFC4A66B,
            },

            # 3066be, 119da4, 6d9dc5, 80ded9, aeecef Cool
            {
                MazeColors.BACKGROUND: 0xFF3066BE,
                MazeColors.WALL: 0xFF119DA4,
                MazeColors.PATH: 0xFF6D9DC5,
                MazeColors.START: 0xFF80DED9,
                MazeColors.END: 0xFFAEECEF,
                MazeColors.LOGO: 0xFF7FDBB6,
            },

            # 476a6f, 519e8a, 7eb09b, c5c9a4, ecbeb4 Soft
            {
                MazeColors.BACKGROUND: 0xFF476A6F,
                MazeColors.WALL: 0xFF519E8A,
                MazeColors.PATH: 0xFF7EB09B,
                MazeColors.START: 0xFFC5C9A4,
                MazeColors.END: 0xFFECBEB4,
                MazeColors.LOGO: 0xFFD9C4AC,
            },
        ]

        self.current_scheme: int = 5
        self.total_schemes: int = len(self.schemes)

    def get(self, color: MazeColors) -> int:
        """Return the integer color value for the given MazeColors key
        in the currently active scheme.

        Args:
            color: A MazeColors enum member identifying which color to
                retrieve from the active scheme.

        Returns:
            The packed integer color value for the requested key.
        """

        return self.schemes[self.current_scheme][color]

    def next_scheme(self) -> None:
        """Advance to the next available color scheme.

        Wraps around to the first scheme when the end of the list is
        reached.

        Returns:
            None
        """

        self.current_scheme = (self.current_scheme + 1) % self.total_schemes
