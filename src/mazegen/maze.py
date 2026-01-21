import sys
from .display.maze_display import MazeDisplay
from .config import Config
from .maze_generator import MazeGenerator


class MazeApp:
    def __init__(self, config_file: str):
        try:
            self.config = Config(config_file)
            self.maze = MazeGenerator(self.config)
            self.maze.generate()

            self.renderer = MazeDisplay(self.maze, self.config)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
