from src.direction import Direction
from src.cell import Cell


class MazeGenerator:
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

    def pathfinding_next_step(self, x: int, y: int) -> tuple[int, int]:
        if not self.path:
            return (x, y)

        direction = self.path[0]
        self.path = self.path[1:]

        if direction == 'N':
            return (x, y - 1)
        elif direction == 'E':
            return (x + 1, y)
        elif direction == 'S':
            return (x, y + 1)
        elif direction == 'W':
            return (x - 1, y)
        else:
            return (x, y)


if __name__ == '__main__':
    maze_data = ''
    with open('maze.txt', 'r') as f:
        maze_data = f.read()

    maze = MazeGenerator(25, 20)
    maze.import_maze(maze_data)
    print(maze.export())
