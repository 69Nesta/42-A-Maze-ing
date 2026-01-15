from random import shuffle
from time import sleep
from enum import Enum

t_point = tuple[int, int]
t_wall = tuple[int, int, int, int]

logo = [[1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]]


OPPOSITE = {
    0: 2,
    2: 0,
    1: 3,
    3: 1
}


class Direction(Enum):
    NORTH: int = 0
    EAST: int = 1
    SOUTH: int = 2
    WEST: int = 3


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: t_point, exit: t_point):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.maze = None
        self.last_direction = None

    def generate(self):
        self.maze = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        center_x = (self.width - len(logo[0])) // 2
        center_y = (self.height - len(logo)) // 2
        for i in range(len(logo)):
            for j in range(len(logo[i])):
                if logo[i][j] == 1:
                    self.maze[int(center_y) + i][int(center_x) + j] = Cell.create(j,i, True, True, True ,True)
        MazeGenerator.back_track(self, self.entry[0], self.entry[1])

    def back_track(self, x, y):

        directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        shuffle(directions)

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

                if self.maze[new_y][new_x] == (0, 0, 0, 0):

                    if (new_x, new_y) == self.exit:
                        self.maze[new_y][new_x] = "q"
                        return

                    if direction == Direction.NORTH:
                        self.maze[y][x] = (1, 0, 0, 0)
                        self.maze[new_y][new_x] = (0, 0, 1, 0)

                    elif direction == Direction.EAST:
                        self.maze[y][x] = (0, 1, 0, 0)
                        self.maze[new_y][new_x] = (0, 0, 0, 1)

                    elif direction == Direction.SOUTH:
                        self.maze[y][x] = (0, 0, 1, 0)
                        self.maze[new_y][new_x] = (1, 0, 0, 0)

                    elif direction == Direction.WEST:
                        self.maze[y][x] = (0, 0, 0, 1)
                        self.maze[new_y][new_x] = (0, 1, 0, 0)

                    # MazeGenerator.display_logo(self)
                    # sleep(0.05)

                    # Récursion
                    self.back_track(new_x, new_y)

    def display_logo(self):
        print("----------------------------")
        for row in self.maze:
            for cell in row:
                print(cell.walls)
            print(",")
        print("----------------------------")


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = {
            Direction.NORTH: False,
            Direction.EAST: False,
            Direction.SOUTH: False,
            Direction.WEST: False,
        }

    def remove_wall(self, direction: Direction):
        self.walls[direction] = False

    def has_wall(self, direction: Direction) -> bool:
        return self.walls[direction]

    def is_full(self):
        return self.walls[Direction.NORTH] and \
               self.walls[Direction.EAST] and \
               self.walls[Direction.SOUTH] and \
               self.walls[Direction.WEST]

    def export(self) -> str:
        bits = [
            int(self.walls[Direction.WEST]),
            int(self.walls[Direction.SOUTH]),
            int(self.walls[Direction.EAST]),
            int(self.walls[Direction.NORTH]),
        ]
        bit_str = ''.join(str(b) for b in bits)
        hex_value = hex(int(bit_str, 2))[2:].upper()
        return hex_value

    def import_cell(self, data: str):
        if data.isdigit():
            bits = f"{int(data):04b}"
        else:
            bits = f"{int(data, 16):04b}"
        self.walls[Direction.NORTH] = bits[3] == '1'
        self.walls[Direction.EAST] = bits[2] == '1'
        self.walls[Direction.SOUTH] = bits[1] == '1'
        self.walls[Direction.WEST] = bits[0] == '1'

    @classmethod
    def create(cls,
               x: int, y: int,
               north: bool, east: bool, south: bool, west: bool
               ) -> 'Cell':
        cell = cls(x, y)
        cell.walls[Direction.NORTH] = north
        cell.walls[Direction.EAST] = east
        cell.walls[Direction.SOUTH] = south
        cell.walls[Direction.WEST] = west
        return cell

maze = MazeGenerator(20, 15, (1, 1), (14, 14))
maze.generate()
maze.display_logo()
