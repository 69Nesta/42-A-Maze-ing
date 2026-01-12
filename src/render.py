from mlx import Mlx


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

        print(self.img)

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


class Renderer:
    WIDTH: int = 800
    HEIGHT: int = 600

    def __init__(self):
        self.current_pixel: int = 0

        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.WIDTH,
            self.HEIGHT,
            "Renderer Window"
        )

        self.image = Image(self.mlx, self.mlx_ptr, self.WIDTH, self.HEIGHT)
        self.render(None)

        self.mlx.mlx_hook(self.win_ptr, 33, 1 << 17, self.close, None)
        self.mlx.mlx_loop(self.mlx_ptr)

    def render(self, _):
        self.image.clear(0xFFFFFFFF)
        self.image.put_pixel(
            self.WIDTH // 2,
            self.HEIGHT // 2,
            0xFF0000FF
        )

        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.image.img,
            0,
            0
        )
        pass

    def close(self, _):
        try:
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        finally:
            try:
                self.mlx.mlx_loop_exit(self.mlx_ptr)
            except Exception:
                pass
        return 0
