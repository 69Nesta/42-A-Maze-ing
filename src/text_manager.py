from mlx import Mlx


class Text:
    def __init__(self, x: int, y: int, color: int, content: str) -> None:
        self.x: int = x
        self.y: int = y
        self.color: int = color
        self.content: str = content


class TextManager:
    def __init__(self, mlx: Mlx, mlx_ptr, win_ptr) -> None:
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.need_update: bool = True
        self.texts: list[Text] = []

    def text_exists(self, x: int, y: int, content: str) -> bool:
        for text in self.texts:
            if text.x == x and text.y == y and text.content == content:
                return True
        return False

    def create_text(self, x: int, y: int, color: int, content: str
                    ) -> Text | None:
        if self.text_exists(x, y, content):
            return None
        text = Text(x, y, color, content)
        self.texts.append(text)
        return text

    def put_texts(self) -> None:
        for text in self.texts:
            self.mlx.mlx_string_put(
                self.mlx_ptr,
                self.win_ptr,
                text.x,
                text.y,
                text.color,
                text.content
            )
