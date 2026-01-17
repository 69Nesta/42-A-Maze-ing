from mlx import Mlx
from enum import Enum
from src.display.image import Image
from src.display.buttons import ButtonManager, Button, ColorSelector
from src.maze import MazeGenerator
from src.direction import Direction
from src.errors import (DisplayMazeToBig)
from src.cell import Cell
from src.display.text_manager import TextManager
from src.display.schemes_colors import (MazeColors, MazeSchemesColors)


class Settings(Enum):
    SHOW_PATHFINDING = 'show_pathfinding'
    CUSTOM_LOGO_COLOR = 'custom_logo_color'


class MazeDisplaySettings:
    def __init__(self, defaults: dict[Settings, bool] = {}):
        self.settings = defaults

    def set(self, key: Settings, value: bool):
        self.settings[key] = value

    def get(self, key: Settings) -> bool | None:
        if key in self.settings:
            return self.settings[key]
        return None

    def toggle(self, key: Settings) -> None:
        if key in self.settings and isinstance(self.settings[key], bool):
            self.settings[key] = not self.settings[key]


class MazeDisplay:
    WIDTH: int
    HEIGHT: int

    MAZE_PADDING: int = 0
    WIDTH_MAZE: int
    WIDTH_PANEL: int

    def __init__(self, maze: MazeGenerator) -> None:
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
        self.first_render: bool = True
        self.start_time: float = 0.0
        self.last_time: float = 0.0
        self.frame_count: int = 0
        self.settings: MazeDisplaySettings = MazeDisplaySettings({
            Settings.SHOW_PATHFINDING: False,
            Settings.CUSTOM_LOGO_COLOR: False,
        })

        self.custom_logo_color: int = 0xFFFF0000

        self.panel: Image = Image(
                self.mlx, self.mlx_ptr,
                self.WIDTH_PANEL,
                self.HEIGHT
            )

        self.texts: TextManager = TextManager(
            self.mlx,
            self.mlx_ptr,
            self.win_ptr
        )

        self.buttons: ButtonManager = ButtonManager(
            self.panel,
            self.WIDTH - self.WIDTH_PANEL,
            self.texts
        )

        self.color_schemes: MazeSchemesColors = MazeSchemesColors()

        total_width: int = self.WIDTH_MAZE - self.MAZE_PADDING
        total_height: int = self.HEIGHT - self.MAZE_PADDING

        cell_width: int = total_width // (self.maze.width * 2 + 1)
        cell_height: int = total_height // (self.maze.height * 2 + 1)

        self.cell_size: int = min(cell_width, cell_height)

        self.total_width: int = self.cell_size * (self.maze.width * 2 + 1)
        self.total_height: int = self.cell_size * (self.maze.height * 2 + 1)

        if cell_width == 0 or cell_height == 0:
            raise DisplayMazeToBig(
                self.maze.width, self.maze.height,
                self.WIDTH_MAZE - self.MAZE_PADDING,
                self.HEIGHT - self.MAZE_PADDING
            )
        else:
            self.maze_image: Image = Image(
                self.mlx, self.mlx_ptr,
                self.total_width,
                self.total_height
            )

        if (self.maze_image.width < self.maze.width * 2 + 1 or
           self.maze_image.height < self.maze.height * 2 + 1):
            raise DisplayMazeToBig(
                self.maze.width, self.maze.height,
                self.WIDTH_MAZE - self.MAZE_PADDING,
                self.HEIGHT - self.MAZE_PADDING
            )

        self.mlx.mlx_hook(self.win_ptr, 33, 1 << 17, self.close, None)
        self.mlx.mlx_key_hook(self.win_ptr, self.key_hook, None)
        self.mlx.mlx_mouse_hook(self.win_ptr, self.mouse_hook, None)
        self.start_render()
        self.mlx.mlx_loop(self.mlx_ptr)

    def close(self, _) -> int:
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

    def start_render(self) -> None:
        # self.render(None)

        # replace with looped render call
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render, None)

    def render(self, _) -> int:
        if (self.panel.need_update):
            self.render_panel()
            self.mlx.mlx_put_image_to_window(
                self.mlx_ptr,
                self.win_ptr,
                self.panel.img,
                self.WIDTH_MAZE,
                0
            )
            self.panel.need_update = False

        if self.texts.need_update:
            self.texts.need_update = False
            self.texts.put_texts()

        if self.maze_image.need_update:
            self.maze_image.need_update = False
            self.render_maze()
            self.mlx.mlx_put_image_to_window(
                self.mlx_ptr,
                self.win_ptr,
                self.maze_image.img,
                self.WIDTH_MAZE // 2 - self.total_width // 2,
                self.HEIGHT // 2 - self.total_height // 2
            )
        if (self.first_render):
            self.first_render = False
        return 0

    def render_panel(self) -> None:
        print("Rendering panel...")
        image: Image = self.panel

        image.draw_rectangle(
            0, 0,
            image.width,
            image.height,
            0xFFCCCCCC
        )

        self.buttons.add_button(
            Button(
                "Regenerate Maze",
                10, 10,
                200, 60,
                0xFFABDAFC,
                0xFFE5FCFF,
                lambda: self.generate_new_maze()
            )
        )

        self.buttons.add_button(
            Button(
                "Change Color Scheme",
                10, 80,
                200, 60,
                0xFFABDAFC,
                0xFFE5FCFF,
                lambda: self.change_color_scheme()
            )
        )

        self.buttons.add_button(
            Button(
                "Toggle Pathfinding",
                10, 150,
                200, 60,
                0xFFABDAFC,
                0xFFE5FCFF,
                lambda: self.toggle_setting(Settings.SHOW_PATHFINDING)
            )
        )

        self.buttons.add_button(
            Button(
                "Exit",
                10, 220,
                200, 60,
                0xFFABDAFC,
                0xFFE5FCFF,
                lambda: self.close(None)
            )
        )

        self.buttons.add_color_selector(
            ColorSelector(
                "Logo Color",
                10, 310,
                100,
                0xFFE5FCFF,
                lambda color: self.set_custom_logo_color(color),
            )
        )

        # image.draw_color_selector(10, 290, 100)
        pass

    def render_maze(self) -> None:
        print("Rendering maze...")
        self.draw_maze()
        if self.settings.get(Settings.SHOW_PATHFINDING):
            self.draw_pathfinding()

    def draw_maze(self) -> None:
        image: Image = self.maze_image
        maze: MazeGenerator = self.maze

        cell_size = self.cell_size

        image.draw_rectangle(
            0, 0,
            cell_size * maze.width * 2 + cell_size,
            cell_size * maze.height * 2 + cell_size,
            self.color_schemes.get(MazeColors.BACKGROUND)
        )

        logo_color = self.color_schemes.get(MazeColors.LOGO)
        if self.settings.get(Settings.CUSTOM_LOGO_COLOR):
            logo_color = self.custom_logo_color

        wall_color = self.color_schemes.get(MazeColors.WALL)

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                self.draw_cell_border(
                    cell,
                    x,
                    y,
                    wall_color
                )
                if cell.is_full():
                    self.draw_cell_fill(
                        x, y,
                        logo_color
                    )

        self.draw_start_end()

    def draw_pathfinding(self) -> None:
        print("Drawing pathfinding...")
        image: Image = self.maze_image
        maze: MazeGenerator = self.maze

        color: int

        if (self.settings.get(Settings.SHOW_PATHFINDING)):
            color = self.color_schemes.get(MazeColors.PATH)
        elif (not self.first_render):
            color = self.color_schemes.get(MazeColors.BACKGROUND)
        else:
            return

        x, y = maze.start
        for step in maze.pathfinding_next_step():
            current_x, current_y = x, y
            x, y, direction = step
            x0, y0, x1, y1, _, _ = self.get_cell_pos(current_x, current_y)

            match direction:
                case Direction.NORTH:
                    image.draw_rectangle(
                        x1, y0,
                        self.cell_size, self.cell_size * 2,
                        color
                    )
                case Direction.EAST:
                    image.draw_rectangle(
                        x1, y1,
                        self.cell_size * 2, self.cell_size,
                        color
                    )
                case Direction.SOUTH:
                    image.draw_rectangle(
                        x1, y1,
                        self.cell_size, self.cell_size * 2,
                        color
                    )
                case Direction.WEST:
                    image.draw_rectangle(
                        x0, y1,
                        self.cell_size * 2, self.cell_size,
                        color
                    )
                case _:
                    break
        self.draw_start_end()
        pass

    def draw_start_end(self) -> None:
        maze: MazeGenerator = self.maze

        sx, sy = maze.start
        ex, ey = maze.end
        self.draw_cell_fill(sx, sy, self.color_schemes.get(MazeColors.START))
        self.draw_cell_fill(ex, ey, self.color_schemes.get(MazeColors.END))

    def generate_new_maze(self) -> None:
        self.maze.generate()
        self.maze_image.need_update = True

    def change_color_scheme(self) -> None:
        self.color_schemes.next_scheme()
        self.maze_image.need_update = True

    def toggle_setting(self, setting: Settings) -> None:
        self.settings.toggle(setting)
        self.maze_image.need_update = True

    def set_custom_logo_color(self, color: int) -> None:
        self.custom_logo_color = color
        self.settings.set(Settings.CUSTOM_LOGO_COLOR, True)
        self.maze_image.need_update = True

    def get_cell_pos(
        self,
        x: int,
        y: int,
    ) -> tuple[int, int, int, int, int, int]:
        cell_size: int = self.cell_size

        x0: int = x * cell_size * 2
        y0: int = y * cell_size * 2

        x1: int = x0 + cell_size
        y1: int = y0 + cell_size

        x2: int = x1 + cell_size
        y2: int = y1 + cell_size
        return (x0, y0, x1, y1, x2, y2)

    def draw_cell_border(
        self,
        cell: Cell,
        x: int,
        y: int,
        color: int
    ) -> None:
        image: Image = self.maze_image
        cell_size: int = self.cell_size
        x0, y0, _, _, x2, y2 = self.get_cell_pos(x, y)

        if cell.has_wall(Direction.NORTH):
            image.draw_rectangle(x0, y0, cell_size * 3, cell_size, color)
        if cell.has_wall(Direction.EAST):
            image.draw_rectangle(x2, y0, cell_size, cell_size * 3, color)
        if cell.has_wall(Direction.SOUTH):
            image.draw_rectangle(x0, y2, cell_size * 3, cell_size, color)
        if cell.has_wall(Direction.WEST):
            image.draw_rectangle(x0, y0, cell_size, cell_size * 3, color)

    def draw_cell_fill(
        self,
        x: int,
        y: int,
        color: int
    ) -> None:
        image: Image = self.maze_image
        cell_size: int = self.cell_size
        _, _, x1, y1, _, _ = self.get_cell_pos(x, y)

        # print(f"Filling cell at ({x}, {y}) -> pixel ({x1}, {y1})")

        image.draw_rectangle(
            x1, y1,
            cell_size, cell_size,
            color
        )

    def mouse_hook(self, btn: int, x: int, y: int, _):
        print("Window clicked.")
        self.buttons.on_click(x - self.WIDTH_MAZE, y)
        return 0

    def key_hook(self, keycode: int, _):
        match keycode:
            case 65307:  # ESC key
                print("Escape key pressed. Exiting...")
                self.close(None)
        return 0
