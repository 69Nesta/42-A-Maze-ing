from mlx import Mlx


class Image:
    def __init__(self,
                 mlx: Mlx,
                 mlx_ptr: int,
                 width: int,
                 height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.img: int = mlx.mlx_new_image(mlx_ptr, width, height)

        buf, bpp, size_line, endian = mlx.mlx_get_data_addr(self.img)

        self.addr: memoryview[int] = buf.cast('B')
        self.bits_per_pixel: int = bpp
        self.size_line: int = size_line
        self.endian: int = endian
        self.need_update: bool = True

    def destroy(self, mlx: Mlx, mlx_ptr: int) -> None:
        mlx.mlx_destroy_image(mlx_ptr, self.img)

    def put_pixel(self, x: int, y: int, color: int) -> None:
        bpp: int = self.bits_per_pixel // 8
        offset: int = y * self.size_line + x * bpp

        if offset < 0 or offset + bpp > len(self.addr):
            raise IndexError("Pixel coordinates out of bounds")

        self.addr[offset:offset + bpp] = \
            color.to_bytes(bpp, 'little')

    def draw_rectangle(self,
                       x: int, y: int,
                       w: int, h: int,
                       color: int) -> None:
        bpp: int = self.bits_per_pixel // 8
        color_bytes: bytes = color.to_bytes(bpp, 'little')

        line_size: int = self.size_line
        rect_row: bytes = color_bytes * w

        base_offset: int = y * line_size + x * bpp

        for j in range(h):
            offset: int = base_offset + j * line_size
            self.addr[offset:offset + w * bpp] = rect_row

    def draw_color_selector(self, x: int, y: int, size: int) -> None:
        for j in range(size):
            for i in range(size):
                t = 255
                r = int((i / (size - 1)) * 255)
                g = int((j / (size - 1)) * 255)
                b = int((1 - ((i + j) / (2 * (size - 1)))) * 255)
                color = (t << 24) | (r << 16) | (g << 8) | b
                self.put_pixel(x + i, y + j, color)

    def draw_line(self,
                  x0: int, y0: int,
                  x1: int, y1: int,
                  color: int) -> None:
        dx: int = abs(x1 - x0)
        dy: int = abs(y1 - y0)
        sx: int = 1 if x0 < x1 else -1
        sy: int = 1 if y0 < y1 else -1
        err: int = dx - dy

        while True:
            self.put_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            err2: int = err * 2
            if err2 > -dy:
                err -= dy
                x0 += sx
            if err2 < dx:
                err += dx
                y0 += sy

    def get_pixel(self, x: int, y: int) -> int:
        bytes_per_pixel: int = self.bits_per_pixel // 8
        offset: int = (y * self.size_line) + (x * bytes_per_pixel)
        pixel_bytes: memoryview[int] = self.addr[
            offset:offset + bytes_per_pixel
        ]
        return int.from_bytes(pixel_bytes, 'little')

    def clear(self, color: int) -> None:
        self.addr[:] = \
            color.to_bytes(self.bits_per_pixel // 8, 'little') \
            * (self.width * self.height)
