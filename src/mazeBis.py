from src.direction import Direction
from src.cell import Cell
from random import shuffle, randint


t_point = tuple[int, int]

logo = [[1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]]


class MazeNewGenerator:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.path = ''

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
                self,
                x: int, y: int
            ) -> tuple[int, int, Direction]:
        if not self.path:
            return (x, y, None)

        direction = self.path[0].capitalize()
        self.path = self.path[1:]

        match direction:
            case 'N':
                return (x, y - 1, Direction.NORTH)
            case 'E':
                return (x + 1, y, Direction.EAST)
            case 'S':
                return (x, y + 1, Direction.SOUTH)
            case 'W':
                return (x - 1, y, Direction.WEST)
            case _:
                return (x, y, None)

    def generate(self, data: str):
        lines = data.strip().splitlines()
        start_coords = tuple(map(int, lines[-3].split(',')))
        end_coords = tuple(map(int, lines[-2].split(',')))
        self.start = start_coords
        self.end = end_coords
        self.path = None

    def display_logo(self):
        center_x = (self.width - len(logo[0])) // 2
        center_y = (self.height - len(logo)) // 2
        for i in range(len(logo)):
            for j in range(len(logo[i])):
                if logo[i][j] == 1:
                    self.grid[int(center_y) + i][int(center_x) + j].is_logo = True

    def solve(self, x, y):
        solution = MazeNewGenerator.back_track_find(self, x, y)
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

    def create(self, y, x):
        next = [self.grid[y][x]]
        self.grid[y][x].is_next = True

        while next:
            next_cell = next.pop(randint(0, len(next)-1))
            if next_cell.x != self.end[0] or next_cell.y != self.end[1]:
                if next_cell.y - 1 >= 0:
                    new = self.grid[next_cell.y - 1][next_cell.x]
                    if not new.is_next and new.is_logo is False:
                        new.is_next = True
                        next.append(new)
                        next_cell.del_north()
                        new.del_south()
                if next_cell.y + 1 < self.height:
                    new = self.grid[next_cell.y + 1][next_cell.x]
                    if not new.is_next and new.is_logo is False:
                        new.is_next = True
                        next.append(new)
                        next_cell.del_south()
                        new.del_north()
                if next_cell.x - 1 >= 0:
                    new = self.grid[next_cell.y][next_cell.x - 1]
                    if not new.is_next and new.is_logo is False:
                        new.is_next = True
                        next.append(new)
                        next_cell.del_west()
                        new.del_east()
                if next_cell.x + 1 < self.width:
                    new = self.grid[next_cell.y][next_cell.x + 1]
                    if not new.is_next and new.is_logo is False:
                        new.is_next = True
                        next.append(new)
                        next_cell.del_east()
                        new.del_west()

