from mlx import Mlx
import time
from src.maze import MazeGenerator


class Button:
    def __init__(self,
                 x: int, y: int,
                 w: int, h: int,
                 label: str,
                 callback: callable = None):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.label = label
        self.callback = callback

    def collision(self, px: int, py: int) -> bool:
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)

    def press(self):
        if self.callback:
            self.callback()


class Text:
    def __init__(self, x: int, y: int, content: str, color: int):
        self.x = x
        self.y = y
        self.content = content
        self.color = color


class Image:
    def __init__(self, mlx: Mlx, mlx_ptr: int, width: int, height: int):
        self.width = width
        self.height = height
        self.img = mlx.mlx_new_image(mlx_ptr, width, height)

        buf, bpp, size_line, endian = mlx.mlx_get_data_addr(self.img)

        self.addr = buf.cast('B')
        self.bits_per_pixel = bpp
        self.size_line = size_line
        self.endian = endian
        self.buttons: list[Button] = []

    def destroy(self, mlx: Mlx, mlx_ptr: int):
        mlx.mlx_destroy_image(mlx_ptr, self.img)

    def put_pixel(self, x: int, y: int, color: int):
        bpp = self.bits_per_pixel // 8
        offset = y * self.size_line + x * bpp

        self.addr[offset:offset + bpp] = \
            color.to_bytes(bpp, 'little')

    def draw_rectangle(self, x: int, y: int, w: int, h: int, color: int):
        for j in range(y, y + h):
            for i in range(x, x + w):
                self.put_pixel(i, j, color)

    def draw_line(self, x0: int, y0: int, x1: int, y1: int, color: int):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.put_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            err2 = err * 2
            if err2 > -dy:
                err -= dy
                x0 += sx
            if err2 < dx:
                err += dx
                y0 += sy

    def get_pixel(self, x: int, y: int) -> int:
        bytes_per_pixel = self.bits_per_pixel // 8
        offset = (y * self.size_line) + (x * bytes_per_pixel)
        pixel_bytes = self.addr[offset:offset + bytes_per_pixel]
        return int.from_bytes(pixel_bytes, 'little')

    def clear(self, color: int):
        for y in range(self.height):
            for x in range(self.width):
                self.put_pixel(x, y, color)

    def create_buttons(
            self,
            x: int, y: int,
            w: int, h: int,
            labels: str,
            color: int,
            callback: callable = None
            ) -> None:
        self.buttons.append(Button(x, y, w, h, labels, callback))
        self.draw_rectangle(x, y, w, h, color)


class Renderer:
    WIDTH: int
    HEIGHT: int

    def __init__(self, maze: MazeGenerator):
        self.current_pixel: int = 0

        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        _, self.WIDTH, self.HEIGHT = self.mlx.mlx_get_screen_size(self.mlx_ptr)

        self.WIDTH = self.WIDTH * 3 // 4
        self.HEIGHT = self.HEIGHT * 3 // 4
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.WIDTH,
            self.HEIGHT,
            "Renderer Window"
        )
        self.maze: MazeGenerator = maze
        self.start_time: float = 0.0
        self.last_time: float = 0.0
        self.frame_count: int = 0
        self.texts: list[Text] = []

        self.image = Image(self.mlx, self.mlx_ptr, self.WIDTH, self.HEIGHT)

        self.mlx.mlx_hook(self.win_ptr, 33, 1 << 17, self.close, None)
        # self.mlx.mlx_hook(self.win_ptr, 10, 1, self.close, None)
        self.mlx.mlx_key_hook(self.win_ptr, self.key_hook, None)
        self.mlx.mlx_mouse_hook(self.win_ptr, self.mouse_hook, None)
        self.start_render()
        self.mlx.mlx_loop(self.mlx_ptr)

    def close(self, _):
        try:
            self.image.destroy(self.mlx, self.mlx_ptr)
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        finally:
            try:
                self.mlx.mlx_loop_exit(self.mlx_ptr)
            except Exception:
                pass
        return 0

    def start_render(self):
        self.init_buttons()
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render, None)

    def stop_render(self):
        self.mlx.mlx_loop_hook(self.mlx_ptr, None, None)

    def create_text(self, x: int, y: int, content: str, color: int) -> None:
        self.texts.append(Text(x, y, content, color))
        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            x,
            y,
            color,
            content
        )

    def create_buttons(
            self,
            x: int, y: int,
            w: int, h: int,
            labels: str,
            color_text: int,
            color_bg: int,
            callback: callable = None
            ) -> None:
        self.image.create_buttons(x, y, w, h, labels, color_bg, callback)
        self.create_text(
            x + 10,
            y + 10,
            labels,
            color_text,
        )

    def init_buttons(self):
        self.create_buttons(10, 40, 80, 30, "Stop", 0xffaaaaaa, 0xff0000ff, (lambda: print(self.maze.export())))

    def render(self, _):
        maze = self.maze
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if self.start_time == 0.0:
            self.start_time = current_time
            elapsed_time = 0.0

        self.image.draw_rectangle(
            10,
            10,
            90,
            20,
            0xff000000
        )

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.image.img,
            0, 0
        )

        for text in self.texts:
            self.mlx.mlx_string_put(
                self.mlx_ptr,
                self.win_ptr,
                text.x,
                text.y,
                text.color,
                text.content
            )

        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            10,
            10,
            0xffffffff,
            f'FPS: {self.frame_count / elapsed_time if elapsed_time else 0:.0f}'
        )
        self.last_time = current_time
        self.frame_count += 1

    def mouse_hook(self, btn, x, y, _):
        print("Window clicked.")
        for button in self.image.buttons:
            if (button.collision(x, y)):
                print(f"Button '{button.label}' clicked.")
                button.press()
        return 0

    def key_hook(self, keycode, _):
        match keycode:
            case 65307:  # ESC key
                print("Escape key pressed. Exiting...")
                self.close(None)
        return 0
