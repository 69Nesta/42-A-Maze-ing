from typing import Generator
from src.direction import Direction
from src.cell import Cell
from src.config import Config, EConfig
from src.algo_prim import Prim
from src.algo_backtrack import Backtrack
from src.types import t_grid, t_path, t_point
from src.coords import Coords
from random import randint
from src.direction import Direction
from random import seed


logo = [[1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]]


class MazeGenerator:
    def __init__(self, config: Config):
        self.config: Config = config
        self.width: int = self.config.get_int(EConfig.WIDTH).get_value()
        self.height: int = self.config.get_int(EConfig.HEIGHT).get_value()
        self.start: t_point = self.config.get_coords(EConfig.ENTRY).get_value()
        self.end: t_point = self.config.get_coords(EConfig.EXIT).get_value()

        self.grid: t_grid
        self.path: t_path
        self.generate_order: list[Coords] = []
        self.generate_order_size: int = 0

        self.algo = Prim(self.width, self.height, self.end)
        # self.algo = Backtrack(self.width, self.height, self.end)

    def init_grid(self):
        self.grid = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]

    def init_path(self):
        self.path = []

    def init_generate_order(self):
        self.generate_order = []

    def get_cell(self, x: int, y: int) -> Cell:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError("Cell coordinates out of bounds")
        return self.grid[y][x]

    def export(self) -> str:
        lines = []
        for row in self.grid:
            line = ''
            for cell in row:
                line += cell.export()
            lines.append(line)
        return '\n'.join(lines)

    def import_maze(self, data: str):
        self.init_grid()
        lines: list[str] = data.strip().splitlines()
        wall_data: list[str] = lines[:-3]
        sx, sy = map(int, lines[-3].split(','))
        start_coords: t_point = (sx, sy)
        ex, ey = map(int, lines[-2].split(','))
        end_coords: t_point = (ex, ey)
        # path_directions: str = lines[-1]

        # Parse wall data
        for y, line in enumerate(wall_data):
            for x, char in enumerate(line):
                print(f"Parsing cell at ({x}, {y}): {char}")
                cell: Cell = self.get_cell(x, y)
                bits: str
                if char.isdigit():
                    bits = f"{int(char):04b}"
                else:
                    bits = f"{int(char, 16):04b}"
                cell.walls[Direction.NORTH] = bits[3] == '1'
                cell.walls[Direction.EAST] = bits[2] == '1'
                cell.walls[Direction.SOUTH] = bits[1] == '1'
                cell.walls[Direction.WEST] = bits[0] == '1'

        self.start = start_coords
        self.end = end_coords
        self.path = []
        self.path = self.a_star_find(ex, ey)
        # for direction in path_directions:
        #     match direction:
        #         case 'N':
        #             self.path.append(Direction.NORTH)
        #         case 'E':
        #             self.path.append(Direction.EAST)
        #         case 'S':
        #             self.path.append(Direction.SOUTH)
        #         case 'W':
        #             self.path.append(Direction.WEST)
        #         case _:
        #             break

    def pathfinding_next_step(
                self
                ) -> Generator[tuple[int, int, Direction], None, None]:
        if not self.start or not self.end or not self.path:
            return
        # x, y = self.start
        for path in self.path:
            x, y, direction = path
            match direction:
                case Direction.NORTH:
                    yield path
                case Direction.EAST:
                    yield path
                case Direction.SOUTH:
                    yield path
                case Direction.WEST:
                    yield path
                case _:
                    yield (x, y, None)

    def get_path_to_index(self, step: int) -> t_path:
        if step < 0 or step >= len(self.path):
            raise IndexError("Path step out of bounds")
        return self.path[:step]

    def generate(self):
        sx, sy = self.start
        ex, ey = self.end

        self.seed = 424
        seed(self.seed)
        self.generate_order.clear()
        self.init_grid()
        self.init_path()
        self.display_logo()

        # self.create(sx, sy)
        self.generate_order += self.algo.create(self.grid, sx, sy)
        self.generate_order += self.undo_perfect(self.grid, sx, sy, ex, ey)
        self.generate_order_size = len(self.generate_order)
        self.solve(ex, ey)

    def display_logo(self):
        center_x = (self.width - len(logo[0])) // 2
        center_y = (self.height - len(logo)) // 2
        for i in range(len(logo)):
            for j in range(len(logo[i])):
                if logo[i][j] == 1:
                    x = int(center_x) + j
                    y = int(center_y) + i

                    self.grid[y][x].is_logo = True
                    self.generate_order.append(Coords(x, y))

    def solve(self, x: int, y: int) -> None:
        self.path = self.a_star_find(x, y)

    def a_star_find(self, x: int, y: int) -> t_path:
        queue: list[tuple[int, int, t_path]] = []
        visited: set[tuple[int, int]] = set()

        queue.append((x, y, []))
        while queue:
            current_x, current_y, path = queue.pop(0)

            if (current_x, current_y) in visited:
                continue
            visited.add((current_x, current_y))

            if (current_x, current_y) == self.start:
                return path[::-1]

            for direction in Direction:
                if self.grid[current_y][current_x].has_wall(direction):
                    continue

                new_x, new_y = current_x, current_y
                new_path = path.copy()
                if direction == Direction.NORTH:
                    new_y -= 1
                    new_path.append((new_x, new_y, Direction.SOUTH))
                elif direction == Direction.EAST:
                    new_x += 1
                    new_path.append((new_x, new_y, Direction.WEST))
                elif direction == Direction.SOUTH:
                    new_y += 1
                    new_path.append((new_x, new_y, Direction.NORTH))
                elif direction == Direction.WEST:
                    new_x -= 1
                    new_path.append((new_x, new_y, Direction.EAST))

                queue.append((new_x, new_y, new_path))

        return []

    def undo_perfect(self, grid: t_grid, sx: int, sy: int, ex: int, ey: int) -> list[Coords]:
        generate_order: list[Coords] = []
        available = []
        for row in self.grid:
            for cell in row:

                nb_wall = 0
                for wall in cell.walls:
                    if cell.walls[wall] is True:
                        nb_wall += 1
                if nb_wall == 3 and cell.x >= 1 and cell.x < self.width - 1 and cell.y >= 1 and cell.y < self.height - 1 :
                    available.append(cell)
        available_iteration = int(len(available) * 0.3)
        for i in range(available_iteration):
            current_cell = available.pop(randint(0, len(available) - 1))
            for wall in current_cell.walls:
                if current_cell.walls[wall] is False:
                    direction = wall
            new_x, new_y = current_cell.x, current_cell.y
            generate_order.append(Coords(new_x, new_y))
            if direction == Direction.NORTH:
                direction = Direction.SOUTH
                new_y += 1

            elif direction == Direction.SOUTH:
                direction = Direction.NORTH
                new_y -= 1

            elif direction == Direction.EAST:
                direction = Direction.WEST
                new_x -= 1

            elif direction == Direction.WEST:
                direction = Direction.EAST
                new_x += 1

            if not grid[new_y][new_x].is_logo and not current_cell.is_undo_perfect and not grid[new_y][new_x].is_undo_perfect:
                generate_order.append(Coords(new_x, new_y))
                current_cell.is_undo_perfect = True
                grid[new_y][new_x].is_undo_perfect = True
                if direction == Direction.NORTH:
                    current_cell.del_north()
                    grid[new_y][new_x].del_south()
                elif direction == Direction.SOUTH:
                    current_cell.del_south()
                    grid[new_y][new_x].del_north()
                elif direction == Direction.EAST:
                    current_cell.del_east()
                    grid[new_y][new_x].del_west()
                elif direction == Direction.WEST:
                    current_cell.del_west()
                    grid[new_y][new_x].del_east()
        return generate_order
