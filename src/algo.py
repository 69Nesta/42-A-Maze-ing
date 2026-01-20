from src.types import t_point, t_grid
from src.coords import Coords


class Algo:
    def __init__(self, width: int, height: int, end: t_point):
        self.end: t_point = end
        self.height: int = height
        self.width: int = width

    def create(self, grid: t_grid, x: int, y: int) -> list[Coords]:
        return []
