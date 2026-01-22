import sys
from .display.maze_display import MazeDisplay
from .config import Config
from .maze_generator import MazeGenerator


class MazeApp:
    """initialize and run the maze renderer.

    Args:
        config_file (str): Path to the configuration file containing
            maze and renderer settings.
    """

    def __init__(self, config_file: str):
        """Initialize the application and start the renderer.

        Args:
            config_file (str): Path to the configuration file.

        Returns:
            None
        """
        try:
            self.config = Config(config_file)
            self.maze = MazeGenerator(self.config)
            self.renderer = MazeDisplay(self.maze, self.config)
            self.renderer.generate_new_maze()
            self.renderer.run()
            # self.maze.generate()

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
