import sys
from src.maze import MazeApp
from src.errors import ConfigError

if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        app = MazeApp(args[0] if args else 'config.txt')
    except ConfigError as e:
        print(f'Error: {e}')
