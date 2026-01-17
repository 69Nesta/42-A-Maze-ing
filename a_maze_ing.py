import sys
# from src.display.maze_display import MazeDisplay
from src.config import Config
from src.errors import ConfigError
from src.maze import MazeGenerator


class AMazeIng:
    def __init__(self, config_file: str):
        self.config = Config(config_file)
        print(self.config.parser.width.get_value())
        # self.maze = MazeGenerator(self.config)
        # maze_data = ''
        # with open(self.config.output_file, 'r') as f:
        #     maze_data = f.read()
        # self.maze.import_maze(maze_data)
        # self.maze.generate()
        # self.renderer = MazeDisplay(self.maze)


if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        app = AMazeIng(args[0] if args else 'config.txt')
    except ConfigError as e:
        print(f'Error: {e}')
