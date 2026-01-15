from src.image import Image
from src.text_manager import TextManager


class Button:
    def __init__(self,
                 label: str,
                 x: int, y: int,
                 width: int, height: int,
                 background: int,
                 text_color: int,
                 callback: callable = None):
        self.label: str = label
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.background: int = background
        self.text_color: int = text_color
        self.callback: callable = callback

    def execute(self):
        if self.callback:
            self.callback()

    def draw(self) -> None:
        self.image.draw_rectangle(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            0xFFAAAAAA
        )
        pass


class ButtonManager:
    def __init__(
            self,
            image: Image,
            offset_x: int,
            text_manager: TextManager
            ) -> None:
        self.image = image
        self.buttons: list[Button] = []
        self.offset_x = offset_x
        self.texts = text_manager

    def add_button(self, button: Button) -> None:
        image = self.image
        self.buttons.append(button)

        x0 = button.x
        y0 = button.y - 5
        w = len(button.label) * 10
        h = 11

        image.draw_rectangle(
            button.x, button.y,
            button.width, button.height,
            button.background
        )
        self.texts.create_text(
            self.offset_x + x0 + (button.width - w) // 2,
            y0 + ((button.height - h) // 2),
            button.text_color,
            button.label
        )

    def get_button_at(self, x: int, y: int) -> Button | None:
        for button in self.buttons:
            if (button.x <= x <= button.x + button.width and
                    button.y <= y <= button.y + button.height):
                return button
        return None

    def on_click(self, x: int, y: int) -> None:
        button = self.get_button_at(x, y)
        if button:
            button.execute()
