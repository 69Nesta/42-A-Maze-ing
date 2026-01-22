from ..types import t_point, t_grid
from ..coords import Coords


class Algo:
    """
    Base class for maze generation algorithms.
    """

    def __init__(self, width: int, height: int, end: t_point):
        """Initialize algorithm with maze dimensions and exit coordinate.

        Args:
            width (int): Maze width.
            height (int): Maze height.
            end (t_point): Exit coordinates.

        Returns:
            None
        """
        self.end: t_point = end
        self.height: int = height
        self.width: int = width

    def create(self, grid: t_grid, x: int, y: int) -> list[Coords]:
        """Generate the maze

        Args:
            grid (t_grid): 2D grid of Cell objects to operate on.
            x (int): Starting x coordinate.
            y (int): Starting y coordinate.

        Returns:
            list[Coords]: Ordered list of coordinates visited during
                generation. The default implementation returns an empty
                list.
        """
        return []
