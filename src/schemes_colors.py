from enum import Enum


class MazeColors(Enum):
    BACKGROUND: int = 0
    WALL: int = 1
    PATH: int = 2
    START: int = 3
    END: int = 4


# Color schemes:
# fff275,ff8c42,ff3c38,a23e48,6c8ead
# 88ccf1,c1dff0,3587a4,2d848a,2d898b
# 242331,533e2d,a27035,b88b4a,ddca7d
# 3066be,119da4,6d9dc5,80ded9,aeecef
# 476a6f,519e8a,7eb09b,c5c9a4,ecbeb4

class MazeSchemesColors:
    def __init__(self):
        self.schemes: list[dict[MazeColors, int]] = [
            # Original scheme
            {
                MazeColors.BACKGROUND: 0xFFD9DBF1,
                MazeColors.WALL: 0xFF7D84B2,
                MazeColors.PATH: 0xFFF5B027,
                MazeColors.START: 0xFFDBF4A7,
                MazeColors.END: 0xFF8E9DCC,
            },

            # fff275, ff8c42, ff3c38, a23e48, 6c8ead
            {
                MazeColors.BACKGROUND: 0xFFFFF275,
                MazeColors.WALL: 0xFFFF8C42,
                MazeColors.PATH: 0xFFFF3C38,
                MazeColors.START: 0xFFA23E48,
                MazeColors.END: 0xFF6C8EAD,
            },

            # 88ccf1, c1dff0, 3587a4, 2d848a, 2d898b
            {
                MazeColors.BACKGROUND: 0xFF88CCF1,
                MazeColors.WALL: 0xFFC1DFF0,
                MazeColors.PATH: 0xFF3587A4,
                MazeColors.START: 0xFF2D848A,
                MazeColors.END: 0xFF2D898B,
            },

            # 242331, 533e2d, a27035, b88b4a, ddca7d
            {
                MazeColors.BACKGROUND: 0xFF242331,
                MazeColors.WALL: 0xFF533E2D,
                MazeColors.PATH: 0xFFA27035,
                MazeColors.START: 0xFFB88B4A,
                MazeColors.END: 0xFFDDCA7D,
            },

            # 3066be, 119da4, 6d9dc5, 80ded9, aeecef
            {
                MazeColors.BACKGROUND: 0xFF3066BE,
                MazeColors.WALL: 0xFF119DA4,
                MazeColors.PATH: 0xFF6D9DC5,
                MazeColors.START: 0xFF80DED9,
                MazeColors.END: 0xFFAEECEF,
            },

            # 476a6f, 519e8a, 7eb09b, c5c9a4, ecbeb4
            {
                MazeColors.BACKGROUND: 0xFF476A6F,
                MazeColors.WALL: 0xFF519E8A,
                MazeColors.PATH: 0xFF7EB09B,
                MazeColors.START: 0xFFC5C9A4,
                MazeColors.END: 0xFFECBEB4,
            },
        ]

        self.current_scheme: int = 0
        self.total_schemes: int = len(self.schemes)

    def get(self, color: MazeColors) -> int:
        return self.schemes[self.current_scheme][color]

    def next_scheme(self) -> None:
        self.current_scheme = (self.current_scheme + 1) % self.total_schemes
