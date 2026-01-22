from typing import Generator, Optional
from .direction import Direction
from .cell import Cell
from .config import Config, EConfig
from .types import t_grid, t_path, t_point
from .coords import Coords
from .algorithms.algo import Algo
from .algorithms.algo_selector import AlgoSelector, EAlgo
from .algorithms.algo_prim import Prim
from .algorithms.algo_backtrack import Backtrack
from random import randint
from random import seed


class MazeGenerator:
    def __init__(
        self,
        config: Config,
        logo_file: Optional[str] = None,
        seed_override: Optional[int] = None,
        algo_override: Optional[EAlgo] = None,
        output_file_override: Optional[str] = None,
    ):
        """Create a MazeGenerator.

        Optional overrides allow caller code (CLI or tests) to change the
        logo file, RNG seed, selected algorithm or output file without
        editing the config file.
        """

        self.config: Config = config
        self.width: int = self.config.get_int(EConfig.WIDTH).get_value()
        self.height: int = self.config.get_int(EConfig.HEIGHT).get_value()
        self.start: t_point = self.config.get_coords(EConfig.ENTRY).get_value()
        self.end: t_point = self.config.get_coords(EConfig.EXIT).get_value()
        if seed_override is not None:
            self.seed = seed_override
        else:
            self.seed = self.config.get_int(EConfig.MAZE_SEED).get_value()
        if output_file_override is not None:
            self.output_file = output_file_override
        else:
            self.output_file = self.config.get_str(
                EConfig.OUTPUT_FILE
            ).get_value()
        if logo_file is not None:
            self.logo_file = logo_file
        else:
            self.logo_file = self.config.get_str(
                EConfig.LOGO_FILE
            ).get_value()
        self.logo: list[list[int]] = self.import_logo(self.logo_file)

        if self.width <= 0 or self.height <= 0:
            raise ValueError("Maze dimensions must be positive integers")
        elif self.width < 5 or self.height < 5:
            raise ValueError("Maze dimensions must be at least 5x5")

        sx, sy = self.start
        ex, ey = self.end
        if (sx < 0 or sx >= self.width
           or sy < 0 or sy >= self.height):
            raise ValueError("Entry coordinates are out of bounds")
        if (ex < 0 or ex >= self.width
           or ey < 0 or ey >= self.height):
            raise ValueError("Exit coordinates are out of bounds")

        self.grid: t_grid = []
        self.path: t_path = []
        self.generate_order: list[Coords] = []
        self.generate_order_size: int = 0

        self.algo: AlgoSelector = AlgoSelector()
        self.algo.register_algo(
            EAlgo.PRIM,
            Prim(self.width, self.height, self.end)
        )
        self.algo.register_algo(
            EAlgo.BACKTRACK,
            Backtrack(self.width, self.height, self.end),
            True
        )
        if algo_override is not None:
            self.algo.set_current_algo(algo_override)

    def update_seed(self, seed_value: int) -> None:
        if (seed_value != 0):
            seed(seed_value)

    def init_grid(self) -> None:
        self.grid = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]

    def init_path(self) -> None:
        self.path = []

    def init_generate_order(self) -> None:
        self.generate_order = []

    def get_cell(self, x: int, y: int) -> Cell:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError("Cell coordinates out of bounds")
        return self.grid[y][x]

    def export(self) -> str:
        grid = []
        for row in self.grid:
            line = ''
            for cell in row:
                line += cell.export()
            grid.append(line)

        sx, sy = self.start
        ex, ey = self.end
        grid.append(f"\n{sx},{sy}")
        grid.append(f"{ex},{ey}")

        direction = ''
        if self.path:
            for step in self.path:
                _, _, dir = step
                match dir:
                    case Direction.NORTH:
                        direction += 'N'
                    case Direction.EAST:
                        direction += 'E'
                    case Direction.SOUTH:
                        direction += 'S'
                    case Direction.WEST:
                        direction += 'W'

        if direction:
            grid.append(direction)
        return '\n'.join(grid) + '\n'

    def import_maze(self, data: str) -> None:
        self.init_grid()
        lines: list[str] = data.strip().splitlines()
        wall_data: list[str] = lines[:-3]
        sx, sy = map(int, lines[-3].split(','))
        start_coords: t_point = (sx, sy)
        ex, ey = map(int, lines[-2].split(','))
        end_coords: t_point = (ex, ey)

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

    @staticmethod
    def import_logo(file: str) -> list[list[int]]:
        logo: list[list[int]] = []
        with open(file, 'r') as all:
            for row in all:
                line: list[int] = []
                for elt in row:
                    if elt == " " or elt == "0":
                        line.append(0)
                    elif elt == '\n':
                        pass
                    else:
                        line.append(1)
                logo.append(line)
        return logo

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

    def generate(self) -> None:
        sx, sy = self.start
        ex, ey = self.end

        self.update_seed(self.seed)

        self.generate_order.clear()
        self.init_grid()
        self.init_path()
        self.display_logo()

        algo: Algo | None = self.algo.get()
        if algo is None:
            raise ValueError("No algorithm selected for maze generation")
        self.generate_order += algo.create(self.grid, sx, sy)
        self.undo_perfect(self.grid)
        self.check_logo()
        self.generate_order_size = len(self.generate_order)
        self.solve(ex, ey)

        try:
            with open(self.output_file, 'w') as f:
                f.write(self.export())
        except Exception as e:
            print(f"Error saving maze to file: {e}")

    def display_logo(self) -> None:
        self.center_x = (self.width - len(self.logo[0])) // 2
        self.center_y = (self.height - len(self.logo)) // 2
        for i in range(len(self.logo)):
            for j in range(len(self.logo[i])):
                x = int(self.center_x) + j
                y = int(self.center_y) + i
                if (x <= 1) or (y <= 1) or (x >= self.width - 2):
                    raise (ValueError("The logo is to big"))
                if self.logo[i][j] == 1:
                    if self.end == (x, y) or self.start == (x, y):
                        raise (ValueError('The logo can t be on the ' +
                                          'exit or the start'))
                    self.grid[y][x].is_logo = True
                    self.generate_order.append(Coords(x, y))
                else:
                    self.grid[y][x].logo_blank = True

    def check_logo(self) -> None:
        for i in range(len(self.logo)):
            for j in range(len(self.logo[i])):
                x = int(self.center_x) + j
                y = int(self.center_y) + i
                if (self.grid[y][x].logo_blank is True):
                    if self.a_star_find(x, y) == []:
                        raise (ValueError('Logo invalid, there must ' +
                                          'be no inaccessible areas'))

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

    def undo_perfect(self, grid: t_grid) -> None:
        available: list[Cell] = []

        for row in self.grid:
            for cell in row:
                nb_wall: int = 0
                for wall in cell.walls:
                    if cell.walls[wall] is True:
                        nb_wall += 1
                if (nb_wall == 3
                   and cell.x >= 1
                   and cell.x < self.width - 1
                   and cell.y >= 1
                   and cell.y < self.height - 1):
                    available.append(cell)

        available_iteration: int = int(len(available) * 0.3)
        for _ in range(available_iteration):
            current_cell: Cell = available.pop(randint(0, len(available) - 1))

            for wall in current_cell.walls:
                if current_cell.walls[wall] is False:
                    direction: Direction = wall

            new_x, new_y = current_cell.x, current_cell.y
            match direction:
                case Direction.NORTH:
                    direction = Direction.SOUTH
                    new_y += 1

                case Direction.SOUTH:
                    direction = Direction.NORTH
                    new_y -= 1

                case Direction.EAST:
                    direction = Direction.WEST
                    new_x -= 1

                case Direction.WEST:
                    direction = Direction.EAST
                    new_x += 1

            if (not grid[new_y][new_x].is_logo
               and not current_cell.is_undo_perfect
               and not grid[new_y][new_x].is_undo_perfect):
                current_cell.is_undo_perfect = True
                grid[new_y][new_x].is_undo_perfect = True

                match direction:
                    case Direction.NORTH:
                        current_cell.del_north()
                        grid[new_y][new_x].del_south()
                    case Direction.SOUTH:
                        current_cell.del_south()
                        grid[new_y][new_x].del_north()
                    case Direction.EAST:
                        current_cell.del_east()
                        grid[new_y][new_x].del_west()
                    case Direction.WEST:
                        current_cell.del_west()
                        grid[new_y][new_x].del_east()
