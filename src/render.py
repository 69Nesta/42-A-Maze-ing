from mlx import Mlx


class Renderer:
    def __init__(self):
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            800,
            600,
            "Renderer Window"
        )
        self.mlx.mlx_loop(self.mlx_ptr)

    def render(self, data):
        print("Rendering data:", data)
