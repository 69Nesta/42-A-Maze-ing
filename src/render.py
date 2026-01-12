from mlx import Mlx


class Renderer:
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        self.current_pixel = 0

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.WIDTH,
            self.HEIGHT,
            "Renderer Window"
        )

        self.img = self.mlx.mlx_new_image(self.mlx_ptr, self.WIDTH,
                                          self.HEIGHT)
        self.addr, self.bpp, self.line_len, self.endian = \
            self.mlx.mlx_get_data_addr(self.img)

        self.mlx.mlx_hook(self.win_ptr, 33, 1 << 17, self.close, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render, None)
        self.mlx.mlx_loop(self.mlx_ptr)

    def render(self, _):
        # for y in range(self.HEIGHT):
        #     for x in range(self.WIDTH):
        #         color = ((x % 256) << 16) | ((y % 256) << 8)
        #         self.img_pixel_put(x, y, color)
        self.img_pixel_put(400, 300, 0xFF0000)  # RED pixel

        # Push image to window
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img, 0, 0
        )
        return 0

    def img_pixel_put(self, x, y, color):
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return

        offset = y * self.line_len + x * (self.bpp // 8)

        # Write color (MLX uses 32-bit int)
        self.addr[offset:offset + 4] = color.to_bytes(4, byteorder='little')

    def img_clear(self):
        self.addr[:] = b'\x00' * (self.line_len * self.HEIGHT)

    def close(self, _):
        try:
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        finally:
            try:
                self.mlx.mlx_loop_exit(self.mlx_ptr)
            except Exception:
                pass
        return 0
