from src.types import t_point, t_grid
from src.coords import Coords
from random import randint, shuffle


class Prim:
    def __init__(self, width: int, height: int, end: t_point):
        self.end: t_point = end
        self.height: int = height
        self.width: int = width

    def create(self, grid: t_grid, x: int, y: int) -> list[Coords]:
        generate_order: list[Coords] = []
        next = [grid[y][x]]
        grid[y][x].is_next = True
        generate_order.append(Coords(x, y))

        while next:
            next_cell = next.pop(randint(0, len(next)-1))
            if next_cell.x != self.end[0] or next_cell.y != self.end[1]:

                def try_north():
                    if next_cell.y - 1 >= 0:
                        new = grid[next_cell.y - 1][next_cell.x]
                        if not new.is_next and new.is_logo is False:
                            new.is_next = True
                            next.append(new)
                            generate_order.append(Coords(new.x, new.y))
                            next_cell.del_north()
                            new.del_south()

                def try_south():
                    if next_cell.y + 1 < self.height:
                        new = grid[next_cell.y + 1][next_cell.x]
                        if not new.is_next and new.is_logo is False:
                            new.is_next = True
                            next.append(new)
                            generate_order.append(Coords(new.x, new.y))
                            next_cell.del_south()
                            new.del_north()

                def try_west():
                    if next_cell.x - 1 >= 0:
                        new = grid[next_cell.y][next_cell.x - 1]
                        if not new.is_next and new.is_logo is False:
                            new.is_next = True
                            next.append(new)
                            generate_order.append(Coords(new.x, new.y))
                            next_cell.del_west()
                            new.del_east()

                def try_east():
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

