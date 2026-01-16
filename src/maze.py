from typing import Generator
from src.direction import Direction
from src.cell import Cell
from src.config import ConfigParser
from random import shuffle
# from time import sleep


t_point = tuple[int, int]

logo = [[1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]]


class MazeGenerator:
    def __init__(self, config: ConfigParser):
        self.config = config
        self.width = self.config.width
        self.height = self.config.width
        self.start = self.config.entry
        self.end = self.config.exit

        self.init_grid()
        self.path = ''

    def init_grid(self):
        self.grid = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
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
        lines = data.strip().splitlines()
        wall_data = lines[:-3]
        start_coords = tuple(map(int, lines[-3].split(',')))
        end_coords = tuple(map(int, lines[-2].split(',')))
        path_directions = lines[-1]

        # Parse wall data
        for y, line in enumerate(wall_data):
            for x, char in enumerate(line):
                cell = self.get_cell(x, y)
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

        self.path = path_directions

    def pathfinding_next_step(
                self
                ) -> Generator[tuple[int, int, Direction], None, None]:
        if not self.start or not self.end or not self.path:
            return (0, 0, None)
        x, y = self.start
        for direction_char in self.path:
            direction = direction_char.capitalize()
            match direction:
                case 'N':
                    y -= 1
                    yield (x, y, Direction.NORTH)
                case 'E':
                    x += 1
                    yield (x, y, Direction.EAST)
                case 'S':
                    y += 1
                    yield (x, y, Direction.SOUTH)
                case 'W':
                    x -= 1
                    yield (x, y, Direction.WEST)
                case _:
                    yield (x, y, None)

    def generate(self):
        sx, sy = self.start
        ex, ey = self.end

        self.path = None
        self.init_grid()
        self.display_logo()
        self.back_track(sx, sy)
        self.solve(ex, ey)

    def display_logo(self):
        center_x = (self.width - len(logo[0])) // 2
        center_y = (self.height - len(logo)) // 2
        for i in range(len(logo)):
            for j in range(len(logo[i])):
                if logo[i][j] == 1:
                    self.grid[
                        int(center_y) + i
                    ][
                        int(center_x) + j
                    ].is_logo = True

    def back_track(self, x, y):
        directions = [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST
        ]
        shuffle(directions)

        for direction in directions:
            new_x = x
            new_y = y

            if direction == Direction.NORTH:
                new_y -= 1
            elif direction == Direction.EAST:
                new_x += 1
            elif direction == Direction.SOUTH:
                new_y += 1
            elif direction == Direction.WEST:
                new_x -= 1

            if (0 <= new_x < self.width and 0 <= new_y < self.height):
                if (self.grid[new_y][new_x].is_full()
                   and not self.grid[new_y][new_x].is_logo):

                    match direction:
                        case Direction.NORTH:
                            self.grid[y][x].del_north()
                            self.grid[new_y][new_x].del_south()

                        case Direction.SOUTH:
                            self.grid[y][x].del_south()
                            self.grid[new_y][new_x].del_north()

                        case Direction.EAST:
                            self.grid[y][x].del_east()
                            self.grid[new_y][new_x].del_west()

                        case Direction.WEST:
                            self.grid[y][x].del_west()
                            self.grid[new_y][new_x].del_east()

                    if (new_x, new_y) == self.end:
                        return

                    self.back_track(new_x, new_y)

    def solve(self, x, y):
        print("gen path")
        path = ""
        solution = MazeGenerator.back_track_find(self, x, y, path)
        print(solution)
        self.path = solution

    def back_track_find(self, x, y, path=""):
        if self.grid[y][x].is_visited:
            return False
        self.grid[y][x].is_visited = True

        if (x, y) == self.end:
            print("end")
            return path

        for direction in Direction:
            if self.grid[y][x].has_wall(direction):
                continue

            new_x, new_y = x, y
            if direction == Direction.NORTH:
                new_y -= 1
                new_path = path + "N"
            elif direction == Direction.EAST:
                new_x += 1
                new_path = path + "E"
            elif direction == Direction.SOUTH:
                new_y += 1
                new_path = path + "S"
            elif direction == Direction.WEST:
                new_x -= 1
                new_path = path + "W"

            result = self.back_track_find(new_x, new_y, new_path)
            if result:
                return result

        return False
