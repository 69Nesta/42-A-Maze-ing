import sys
from mazegen import MazeApp

if __name__ == '__main__':
    args = sys.argv[1:]
    MazeApp(args[0] if args else 'config.txt')
