from mlx import Mlx
from src.image import Image
from src.maze import MazeGenerator
from src.direction import Direction
from src.errors import (DisplayMazeToBig)


class MazeDisplay:
    WIDTH: int
    HEIGHT: int

    MAZE_PADDING: int = 20
    WIDTH_MAZE: int
    WIDTH_PANEL: int

    def __init__(self, maze):
        self.maze = maze

        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        _, screen_w, screen_h = self.mlx.mlx_get_screen_size(self.mlx_ptr)

        self.WIDTH = screen_w * 3 // 4
        self.HEIGHT = screen_h * 3 // 4
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.WIDTH,
            self.HEIGHT,
            "A Maze Ing"
        )
        self.WIDTH_MAZE = self.WIDTH * 3 // 4
        self.WIDTH_PANEL = self.WIDTH - self.WIDTH_MAZE
        self.maze: MazeGenerator = maze
        self.start_time: float = 0.0
        self.last_time: float = 0.0
        self.frame_count: int = 0

        self.panel = Image(
                self.mlx, self.mlx_ptr,
                self.WIDTH_PANEL,
                self.HEIGHT
            )
        self.maze_image = Image(
                self.mlx, self.mlx_ptr,
                self.WIDTH_MAZE - self.MAZE_PADDING,
                self.HEIGHT - self.MAZE_PADDING
            )

        if (self.maze_image.width < self.maze.width or self.maze_image.height < self.maze.height):
            raise DisplayMazeToBig(
                self.maze.width, self.maze.height,
                self.WIDTH_MAZE - self.MAZE_PADDING, self.HEIGHT - self.MAZE_PADDING
            )

        self.mlx.mlx_hook(self.win_ptr, 33, 1 << 17, self.close, None)
        self.mlx.mlx_key_hook(self.win_ptr, self.key_hook, None)
        self.mlx.mlx_mouse_hook(self.win_ptr, self.mouse_hook, None)
        self.start_render()
        self.mlx.mlx_loop(self.mlx_ptr)

    def close(self, _):
        try:
            self.panel.destroy(self.mlx, self.mlx_ptr)
            self.maze_image.destroy(self.mlx, self.mlx_ptr)
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        finally:
            try:
                self.mlx.mlx_loop_exit(self.mlx_ptr)
            except Exception:
                pass
        return 0

    def start_render(self):
        # temporary single render call
        self.render_maze()
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.maze_image.img,
            self.MAZE_PADDING // 2, self.MAZE_PADDING // 2
        )

        # replace with looped render call
        # self.mlx.mlx_loop_hook(self.mlx_ptr, self.render, None)

    def render(self, _):
        self.render_panel()
        self.render_maze()

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.panel.img,
            self.WIDTH_MAZE, 0
        )
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.maze_image.img,
            self.MAZE_PADDING // 2, self.MAZE_PADDING // 2
        )
        return 0

    def render_panel(self):
        # image = self.panel
        pass

    def render_maze(self):
        image = self.maze_image
        maze = self.maze

        cell_width = image.width // maze.width
        cell_height = image.height // maze.height
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                # top left corner
                x0 = x * cell_width
                y0 = y * cell_height
                # bottom right corner
                x1 = x0 + cell_width - 1
                y1 = y0 + cell_height - 1

                if cell.has_wall(Direction.NORTH):
                    image.draw_line(x0, y0, x1, y0, 0xFF0000FF)
                if cell.has_wall(Direction.EAST):
                    image.draw_line(x1, y0, x1, y1, 0x00FF00FF)
                if cell.has_wall(Direction.SOUTH):
                    image.draw_line(x0, y1, x1, y1, 0x0000FFFF)
                if cell.has_wall(Direction.WEST):
                    image.draw_line(x0, y0, x0, y1, 0xFFFF00FF)

        maze.start
        pass

    def mouse_hook(self, btn, x, y, _):
        print("Window clicked.")
        # for button in self.buttons:
        #     if (button.collision(x, y)):
        #         print(f"Button '{button.label}' clicked.")
        #         button.press()
        return 0

    def key_hook(self, keycode, _):
        match keycode:
            case 65307:  # ESC key
                print("Escape key pressed. Exiting...")
                self.close(None)
        return 0
