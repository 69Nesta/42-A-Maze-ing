from .algo import Algo
from ..types import t_point, t_grid
from ..coords import Coords
from random import randint


class Prim(Algo):
    """Prim's randomized maze generation algorithm.

    Args:
        width (int): Width of the maze.
        height (int): Height of the maze.
        end (t_point): Exit coordinates.
    """

    def __init__(self, width: int, height: int, end: t_point) -> None:
        """Initialize the Prim algorithm instance.

        Args:
            width (int): Maze width.
            height (int): Maze height.
            end (t_point): Exit coordinates.
        Returns:
            None
        """
        super().__init__(width, height, end)

    def create(self, grid: t_grid, x: int, y: int) -> list[Coords]:
        """Generate the entire perfect maze by using the Prim
        algorithm

        Args:
            grid (t_grid): 2D grid of Cell objects to operate on.
            x (int): Starting x coordinate.
            y (int): Starting y coordinate.

        Returns:
            list[Coords]: Ordered list of coordinates visited or added
                to the frontier during generation.
        """
        generate_order: list[Coords] = []
        next = [grid[y][x]]
        grid[y][x].is_next = True
        generate_order.append(Coords(x, y))

        while next:
            next_cell = next.pop(randint(0, len(next)-1))
            if next_cell.x != self.end[0] or next_cell.y != self.end[1]:

                def try_north() -> None:
                    if next_cell.y - 1 >= 0:
                        new = grid[next_cell.y - 1][next_cell.x]
                        if not new.is_next and new.is_logo is False:
                            new.is_next = True
                            next.append(new)
                            generate_order.append(Coords(new.x, new.y))
                            next_cell.del_north()
                            new.del_south()

                def try_south() -> None:
                    if next_cell.y + 1 < self.height:
                        new = grid[next_cell.y + 1][next_cell.x]
                        if not new.is_next and new.is_logo is False:
                            new.is_next = True
                            next.append(new)
                            generate_order.append(Coords(new.x, new.y))
                            next_cell.del_south()
                            new.del_north()

                def try_west() -> None:
                    if next_cell.x - 1 >= 0:
                        new = grid[next_cell.y][next_cell.x - 1]
                        if not new.is_next and new.is_logo is False:
                            new.is_next = True
                            next.append(new)
                            generate_order.append(Coords(new.x, new.y))
                            next_cell.del_west()
                            new.del_east()

                def try_east() -> None:
                    if next_cell.x + 1 < self.width:
                        new = grid[next_cell.y][next_cell.x + 1]
                        if not new.is_next and new.is_logo is False:
                            new.is_next = True
                            next.append(new)
                            generate_order.append(Coords(new.x, new.y))
                            next_cell.del_east()
                            new.del_west()
                options = [try_north, try_south, try_west, try_east]
                for try_path in options:
                    try_path()
        return generate_order
