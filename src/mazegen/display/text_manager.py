from typing import Any
from mlx import Mlx


class Text:
    def __init__(self, x: int, y: int, color: int, content: str) -> None:
        self.x: int = x
        self.y: int = y
        self.color: int = color
        self.content: str = content
        self.need_update: bool = True


class TextManager:
    def __init__(self, mlx: Mlx, mlx_ptr: Any, win_ptr: Any) -> None:
        self.mlx: Mlx = mlx
        self.mlx_ptr: Any = mlx_ptr
        self.win_ptr: Any = win_ptr
        self.texts: dict[str, Text] = {}
        self.need_update: bool = True

    def text_exists(self, id: str) -> bool:
        for text_id in self.texts.keys():
            if text_id == id:
                return True
        return False

    def create_text(self, id: str, x: int, y: int, color: int, content: str
                    ) -> Text | None:
        if self.text_exists(id):
            return None
        text: Text = Text(x, y, color, content)
        self.texts[id] = text
        self.need_update = True
        return text

    def put_texts_in(self, x: int, y: int, w: int, h: int) -> None:
        for text in self.texts.values():
            if (x <= text.x <= x + w - 1 and
                    y <= text.y <= y + h - 1):
                self.mlx.mlx_string_put(
                    self.mlx_ptr,
                    self.win_ptr,
                    text.x,
                    text.y,
                    text.color,
                    text.content
                )

    def put_texts(self, force: bool = False) -> None:
        for text in self.texts.values():
            if text.need_update or force:
                self.mlx.mlx_string_put(
                    self.mlx_ptr,
                    self.win_ptr,
                    text.x,
                    text.y,
                    text.color,
                    text.content
                )
                text.need_update = False
        self.need_update = False

    def need_update_texts(self, force: bool = False) -> bool:
        if force:
            for text in self.texts.values():
                if text.need_update:
                    return True
            return False
        else:
            return self.need_update

    def update_text(self, id: str, new_content: str
                    ) -> bool:
        for text_id, text in self.texts.items():
            if text_id == id:
                text.content = new_content
                text.need_update = True
                self.need_update = True
                return True
        return False
