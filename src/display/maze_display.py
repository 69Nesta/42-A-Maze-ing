import time
from mlx import Mlx
from enum import Enum
from ..algo_selector import EAlgo
from ..config import Config, EConfig
from .image import Image
from .buttons import (
    ButtonManager, Button, ColorSelector, Selector, SelectorButton
)
from ..maze_generator import MazeGenerator
from ..direction import Direction
from ..errors import (DisplayMazeToBig)
from ..cell import Cell
from .text_manager import TextManager
from .schemes_colors import (MazeColors, MazeSchemesColors)
from .animation_state import AnimationState
from ..debug import Debug


class Settings(Enum):
    SHOW_FPS = 'show_fps'
    SHOW_PATHFINDING = 'show_pathfinding'
    CUSTOM_LOGO_COLOR = 'custom_logo_color'
    ANIMATE_MAZE_GENERATION = 'animate_maze_generation'
    ANIMATE_PATHFINDING = 'animate_pathfinding'


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

    def __init__(self, maze: MazeGenerator, config: Config) -> None:
        self.config: Config = config
        self.debug: Debug = Debug(config)
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
            Settings.SHOW_FPS: True,
            Settings.SHOW_PATHFINDING: False,
            Settings.CUSTOM_LOGO_COLOR: False,
            Settings.ANIMATE_MAZE_GENERATION:
                config.get_bool(EConfig.ANIMATE_MAZE_GENERATION).get_value(),
            Settings.ANIMATE_PATHFINDING:
                config.get_bool(EConfig.ANIMATE_MAZE_SOLVING).get_value(),
        })

        self.custom_logo_color: int = 0xFFFF0000

        self.background_image = Image(
            self.mlx, self.mlx_ptr,
            self.WIDTH - self.WIDTH_PANEL,
            self.HEIGHT
        )

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
            self.path_image: Image = Image(
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
        self.maze_animation: AnimationState = AnimationState(
            config.get_float(EConfig.MAZE_GENERATION_SPEED).get_value(),
            self.maze.generate_order_size
        )

        self.path_animation: AnimationState = AnimationState(
            config.get_float(EConfig.MAZE_SOLVING_SPEED).get_value(),
            len(self.maze.path)
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
        self.start_time = time.time()
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render, None)

    def render(self, _) -> int:
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        fps = 1.0 / elapsed_time if elapsed_time > 0 else 0.0

        if (self.first_render):
            self.initialize()

        if (self.panel.need_update):
            self.render_panel()
            self.panel.need_update = False
            self.mlx.mlx_put_image_to_window(
                self.mlx_ptr,
                self.win_ptr,
                self.panel.img,
                self.WIDTH_MAZE,
                0
            )
            if not self.first_render:
                self.texts.put_texts_in(
                    self.WIDTH_MAZE,
                    0,
                    self.WIDTH_PANEL,
                    self.HEIGHT
                )

        if (self.background_image.need_update):
            self.render_background()
            self.background_image.need_update = False

        self.render_fps(fps)
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.background_image.img,
            0,
            0
        )

        if self.texts.need_update_texts():
            self.texts.put_texts()

        if self.maze_image.need_update:
            self.maze_image.need_update = False
            self.render_maze(current_time)

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.maze_image.img,
            self.WIDTH_MAZE // 2 - self.total_width // 2,
            self.HEIGHT // 2 - self.total_height // 2
        )

        if self.path_image.need_update:
            self.path_image.need_update = False
            self.render_pathfinding(current_time)

        if (self.settings.get(Settings.SHOW_PATHFINDING)):
            self.mlx.mlx_put_image_to_window(
                self.mlx_ptr,
                self.win_ptr,
                self.path_image.img,
                self.WIDTH_MAZE // 2 - self.total_width // 2,
                self.HEIGHT // 2 - self.total_height // 2
            )

        if (self.first_render):
            self.first_render = False
        self.frame_count += 1
        self.last_time = current_time
        return 0

    def render_fps(self, fps: float) -> None:
        if not self.settings.get(Settings.SHOW_FPS):
            return
        self.background_image.draw_rectangle(
            10, 0,
            70,
            20,
            self.color_schemes.get(MazeColors.BACKGROUND)
        )
        self.texts.update_text(
            'fps_counter',
            f"FPS: {fps:.0f}"
        )

    def render_background(self) -> None:
        self.debug.print("Rendering background...")
        image: Image = self.background_image

        if not image.need_update:
            return
        image.clear(self.color_schemes.get(MazeColors.BACKGROUND))

    def initialize(self) -> None:
        nb_elements = 6
        nb_buttons = 4

        button_width = 350
        button_height = 90

        color_selector_size = 150
        algo_selector_height = 50 + 20 + 20

        total_height = 0
        total_height += algo_selector_height
        total_height += button_height * nb_buttons
        total_height += color_selector_size

        spaceing_h = 30

        total_height_spaceing = spaceing_h * nb_elements + total_height

        selector_gap_w = 10
        selector_btn_width = (self.WIDTH_PANEL - (
            100 if self.WIDTH_PANEL > 700 else 0
        )) // 2
        selector_btn_width -= selector_gap_w
        selector_btn_height = 50
        x_selector = self.WIDTH_PANEL // 2 - (
            (selector_btn_width * 2 + selector_gap_w) // 2
        )

        current_total_height = (self.HEIGHT // 2)
        current_total_height -= total_height_spaceing // 2
        current_total_height += 20
        self.buttons.add_selector(
            'maze_algorithm',
            Selector(
                self.panel,
                'Maze Algorithm',
                x_selector, current_total_height,
                [
                    SelectorButton(
                        'Backtracker',
                        x_selector, current_total_height + 20,
                        selector_btn_width, selector_btn_height,
                        0xFF564E58,
                        0xFF252627,
                        0xFFF2EFE9,
                        0xFFE5FCFF,
                        lambda _: self.change_algo(EAlgo.BACKTRACK)
                    ),
                    SelectorButton(
                        'Prim',
                        x_selector + selector_btn_width + selector_gap_w,
                        current_total_height + 20,
                        selector_btn_width, selector_btn_height,
                        0xFF564E58,
                        0xFF252627,
                        0xFFF2EFE9,
                        0xFFE5FCFF,
                        lambda _: self.change_algo(EAlgo.PRIM)
                    )
                ],
                0,
                0xFFE5FCFF,
                None
            )
        )
        current_total_height += algo_selector_height + spaceing_h

        button_x = self.WIDTH_PANEL // 2 - button_width // 2
        self.buttons.add_button(
            'regenerate_maze',
            Button(
                "Regenerate Maze",
                button_x, current_total_height,
                button_width, button_height,
                0xFF40798C,
                0xFFE5FCFF,
                lambda: self.generate_new_maze()
            )
        )
        current_total_height += button_height + spaceing_h

        self.buttons.add_button(
            'change_color_scheme',
            Button(
                "Change Color Scheme",
                button_x, current_total_height,
                button_width, button_height,
                0xFF98D9C2,
                0xFFE5FCFF,
                lambda: self.change_color_scheme()
            )
        )
        current_total_height += button_height + spaceing_h

        self.buttons.add_button(
            'toggle_pathfinding',
            Button(
                "Toggle Pathfinding",
                button_x, current_total_height,
                button_width, button_height,
                0xFFF19A3E,
                0xFFE5FCFF,
                lambda: self.toggle_pathfinding()
            )
        )
        current_total_height += button_height + spaceing_h

        self.buttons.add_button(
            'exit',
            Button(
                "Exit",
                button_x, current_total_height,
                button_width, button_height,
                0xFF403233,
                0xFFE5FCFF,
                lambda: self.exit_display()
            )
        )
        current_total_height += button_height + spaceing_h

        x_color = self.WIDTH_PANEL // 2 - color_selector_size // 2
        self.buttons.add_color_selector(
            'custom_logo_color',
            ColorSelector(
                "Logo Color",
                x_color, current_total_height,
                color_selector_size,
                0xFFE5FCFF,
                lambda color: self.set_custom_logo_color(color),
            )
        )

        if (self.settings.get(Settings.SHOW_FPS)):
            self.texts.create_text(
                'fps_counter',
                10,
                0,
                0xFFFFFFFF,
                "FPS: 0"
            )

    def render_panel(self) -> None:
        self.debug.print("Rendering panel...")
        image: Image = self.panel
        buttons: ButtonManager = self.buttons

        image.draw_rectangle(
            0, 0,
            image.width,
            image.height,
            self.color_schemes.get(MazeColors.BACKGROUND)
        )
        buttons.draw_buttons()
        self.texts.need_update = True

    def render_maze(self, current_time: float) -> None:
        settings: MazeDisplaySettings = self.settings

        if (settings.get(Settings.ANIMATE_MAZE_GENERATION) and
           not self.maze_animation.finished):
            self.draw_maze_animation(current_time)
        else:
            self.draw_maze()

    def render_pathfinding(self, current_time: float) -> None:
        settings: MazeDisplaySettings = self.settings

        if (not settings.get(Settings.SHOW_PATHFINDING)):
            return
        if (settings.get(Settings.ANIMATE_PATHFINDING) and
           not self.path_animation.finished):
            self.draw_pathfinding_animate(current_time)
        else:
            self.draw_pathfinding()

    def draw_maze(self) -> None:
        image: Image = self.maze_image
        maze: MazeGenerator = self.maze

        image.clear(self.color_schemes.get(MazeColors.BACKGROUND))

        logo_color: int = self.color_schemes.get(MazeColors.LOGO)
        if self.settings.get(Settings.CUSTOM_LOGO_COLOR):
            logo_color = self.custom_logo_color

        wall_color: int = self.color_schemes.get(MazeColors.WALL)
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

    def draw_maze_animation(self, current_time) -> None:
        maze: MazeGenerator = self.maze

        logo_color: int = self.color_schemes.get(MazeColors.LOGO)
        if self.settings.get(Settings.CUSTOM_LOGO_COLOR):
            logo_color = self.custom_logo_color
        wall_color: int = self.color_schemes.get(MazeColors.WALL)
        if not self.maze_animation.started:
            self.maze_animation.start(current_time)
        if self.maze_animation.update(current_time):
            step_index = self.maze_animation.get_next_step()
            if step_index is None:
                self.maze_animation.stop()
                self.draw_start_end()
                return
            x, y = (
                maze.generate_order[step_index].x,
                maze.generate_order[step_index].y
            )
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
            match (x, y):
                case maze.start:
                    self.draw_start()
                case maze.end:
                    self.draw_end()

        if not self.maze_animation.finished:
            self.maze_image.need_update = True

    def redraw_middle_maze_animation(self) -> None:
        maze: MazeGenerator = self.maze
        image: Image = self.maze_image

        image.clear(self.color_schemes.get(MazeColors.BACKGROUND))

        logo_color: int = self.color_schemes.get(MazeColors.LOGO)
        if self.settings.get(Settings.CUSTOM_LOGO_COLOR):
            logo_color = self.custom_logo_color
        wall_color: int = self.color_schemes.get(MazeColors.WALL)

        for step_index in range(0, self.maze_animation.index):
            x, y = (
                maze.generate_order[step_index].x,
                maze.generate_order[step_index].y
            )
            cell = maze.get_cell(x, y)
            self.draw_cell_animate(
                x, y,
                cell,
                wall_color, logo_color
            )

    def draw_pathfinding_cell(
                self,
                x: int,
                y: int,
                direction: Direction
            ) -> None:
        image: Image = self.path_image
        cellsize: int = self.cell_size
        x0, y0, x1, y1, _, _ = self.get_cell_pos(x, y)

        color: int = self.color_schemes.get(MazeColors.PATH)

        match direction:
            case Direction.NORTH:
                image.draw_rectangle(
                    x1, y0,
                    cellsize, cellsize * 2,
                    color
                )
            case Direction.EAST:
                image.draw_rectangle(
                    x1, y1,
                    cellsize * 2, cellsize,
                    color
                )
            case Direction.SOUTH:
                image.draw_rectangle(
                    x1, y1,
                    cellsize, cellsize * 2,
                    color
                )
            case Direction.WEST:
                image.draw_rectangle(
                    x0, y1,
                    cellsize * 2, cellsize,
                    color
                )

        if (x, y) == self.maze.start:
            image.draw_rectangle(
                x1, y1,
                cellsize, cellsize,
                self.color_schemes.get(MazeColors.START)
            )

        if (x, y) == self.maze.end:
            image.draw_rectangle(
                x1, y1,
                cellsize, cellsize,
                self.color_schemes.get(MazeColors.END)
            )

    def draw_pathfinding(self) -> None:
        maze: MazeGenerator = self.maze

        for idx, step in enumerate(maze.path):
            if (self.path_animation.started
               and idx >= self.path_animation.index):
                break
            x, y, direction = step
            self.draw_pathfinding_cell(x, y, direction)
        self.draw_start_end()

    def draw_pathfinding_animate(self, current_time: float) -> None:
        maze: MazeGenerator = self.maze
        animation: AnimationState = self.path_animation

        if not animation.started and not animation.finished:
            animation.start(current_time)
        if animation.update(current_time):
            step_index = animation.get_next_step()
            if step_index is None:
                animation.stop()
                self.draw_pathfinding()
                return
            x, y, direction = maze.path[step_index]
            self.draw_pathfinding_cell(x, y, direction)

        if not animation.finished:
            self.path_image.need_update = True

    def draw_cell_animate(
                self,
                x: int, y: int,
                cell: Cell,
                wall_color: int, logo_color: int
            ) -> None:
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
        match (x, y):
            case self.maze.start:
                self.draw_start()
            case self.maze.end:
                self.draw_end()

    def draw_start(self) -> None:
        maze: MazeGenerator = self.maze

        sx, sy = maze.start
        self.draw_cell_fill(sx, sy, self.color_schemes.get(MazeColors.START))

    def draw_end(self) -> None:
        maze: MazeGenerator = self.maze

        ex, ey = maze.end
        self.draw_cell_fill(ex, ey, self.color_schemes.get(MazeColors.END))

    def draw_start_end(self) -> None:
        self.draw_start()
        self.draw_end()

    def change_algo(self, algo: EAlgo) -> None:
        self.debug.print('Changing maze algorithm...')
        self.maze.algo.set_current_algo(algo)

    def generate_new_maze(self) -> None:
        self.debug.print('Generating new maze...')
        settings: MazeDisplaySettings = self.settings
        self.maze.generate()
        self.maze_animation.reset()
        self.maze_animation.max_step = len(self.maze.generate_order)

        self.maze_image.clear(self.color_schemes.get(MazeColors.BACKGROUND))
        self.maze_image.need_update = True
        if (settings.get(Settings.ANIMATE_MAZE_GENERATION)):
            settings.set(Settings.SHOW_PATHFINDING, False)

        if (settings.get(Settings.ANIMATE_PATHFINDING)):
            self.path_animation.reset()
            self.path_animation.max_step = len(self.maze.path)
            self.path_image.clear(0x00000000)
            self.path_image.need_update = True

    def change_color_scheme(self) -> None:
        self.debug.print('Changing color scheme...')
        self.color_schemes.next_scheme()
        if (self.settings.get(Settings.ANIMATE_MAZE_GENERATION)
           and not self.maze_animation.finished):
            self.redraw_middle_maze_animation()
        if (self.settings.get(Settings.SHOW_PATHFINDING)
           and self.settings.get(Settings.ANIMATE_PATHFINDING)):
            self.draw_pathfinding()
        self.panel.need_update = True
        self.maze_image.need_update = True
        self.background_image.need_update = True

    def toggle_pathfinding(self) -> None:
        self.debug.print('Toggling pathfinding...')
        settings: MazeDisplaySettings = self.settings
        if (settings.get(Settings.ANIMATE_MAZE_GENERATION)
           and not self.maze_animation.finished):
            return

        settings.toggle(Settings.SHOW_PATHFINDING)

        if (settings.get(Settings.SHOW_PATHFINDING)):
            self.path_animation.reset()
            self.path_animation.max_step = len(self.maze.path)
            self.path_image.clear(0x00000000)
            self.path_image.need_update = True

    def toggle_setting(self, setting: Settings) -> None:
        self.settings.toggle(setting)
        self.maze_image.need_update = True

    def set_custom_logo_color(self, color: int) -> None:
        self.debug.print('Setting custom logo color...')
        self.custom_logo_color = color
        self.settings.set(Settings.CUSTOM_LOGO_COLOR, True)
        self.maze_image.need_update = True

    def exit_display(self) -> None:
        self.debug.print('Exiting display...')
        self.close(None)

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

    def mouse_hook(self, btn: int, x: int, y: int, _) -> int:
        self.buttons.on_click(x - self.WIDTH_MAZE, y)
        return 0

    def key_hook(self, keycode: int, _) -> int:
        match keycode:
            case 65307:  # ESC key
                self.debug.print("Escape key pressed. Exiting...")
                self.close(None)
        return 0
