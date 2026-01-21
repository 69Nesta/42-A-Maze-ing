from ..types import t_point, t_grid
from ..direction import Direction
from ..coords import Coords
from .algo import Algo
from random import shuffle


class Backtrack(Algo):
    def __init__(self, width: int, height: int, end: t_point):
        super().__init__(width, height, end)

    def create(self, grid: t_grid, x: int, y: int) -> list[Coords]:
        generate_order: list[Coords] = []
        stack = [(x, y)]
        generate_order.append(Coords(x, y))
        while stack:
            x, y = stack[-1]
            directions = [
                Direction.NORTH,
                Direction.EAST,
                Direction.SOUTH,
                Direction.WEST
                ]
            shuffle(directions)
            moved = False

            for direction in directions:
                new_x, new_y = x, y

                if direction == Direction.NORTH:
                    new_y -= 1
                elif direction == Direction.EAST:
                    new_x += 1
                elif direction == Direction.SOUTH:
                    new_y += 1
                elif direction == Direction.WEST:
                    new_x -= 1

                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    if grid[new_y][new_x].is_full():
                        if not grid[new_y][new_x].is_logo:
                            if direction == Direction.NORTH:
                                grid[y][x].del_north()
                                grid[new_y][new_x].del_south()
                            elif direction == Direction.SOUTH:
                                grid[y][x].del_south()
                                grid[new_y][new_x].del_north()
                            elif direction == Direction.EAST:
                                grid[y][x].del_east()
                                grid[new_y][new_x].del_west()
                            elif direction == Direction.WEST:
                                grid[y][x].del_west()
                                grid[new_y][new_x].del_east()
                            if (new_x, new_y) == self.end:
                                break
                            generate_order.append(Coords(new_x, new_y))
                            stack.append((new_x, new_y))
                            moved = True
                            break
            if not moved:
                stack.pop()
        return generate_order
