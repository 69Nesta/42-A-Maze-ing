# from src.config import ConfigParser
# from src.errors import (ConfigError)
from src.render import Renderer


# if __name__ == '__main__':
#     try:
#         ConfigParser('config.txt')
#     except ConfigError as e:
#         print(f'Error: {e}')

if __name__ == '__main__':
    renderer = Renderer()
    # renderer.render("Hello, World!")
