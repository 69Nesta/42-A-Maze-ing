from src.display.image import Image
from src.display.text_manager import TextManager


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


class ColorSelector:
    def __init__(self,
                 label: str,
                 x: int, y: int,
                 size: int,
                 label_color: int,
                 callback: callable = None):
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.label: str = label
        self.label_color: int = label_color
        self.callback: callable = callback
        self.offset_y: int = 20

    def collide(self, x: int, y: int) -> bool:
        offset_y = self.offset_y
        return (self.x <= x <= self.x + self.size - 1 and
                self.y + offset_y <= y <= self.y + offset_y + self.size - 1)

    def execute(self, color: int):
        if self.callback:
            self.callback(color)


class ButtonManager:
    def __init__(
            self,
            image: Image,
            offset_x: int,
            text_manager: TextManager
            ) -> None:
        self.image = image
        self.buttons: list[Button] = []
        self.selectors: list[ColorSelector] = []
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

    def add_color_selector(self, selector: ColorSelector) -> None:
        image = self.image
        size = selector.size

        self.selectors.append(selector)
        image.draw_color_selector(
            selector.x, selector.y + selector.offset_y,
            size)
        self.texts.create_text(
            self.offset_x + selector.x,
            selector.y - 5,
            selector.label_color,
            selector.label
        )

    def get_button_at(self, x: int, y: int) -> Button | None:
        for button in self.buttons:
            if (button.x <= x <= button.x + button.width and
                    button.y <= y <= button.y + button.height):
                return button
        return None

    def get_selector_at(self, x: int, y: int) -> ColorSelector | None:
        for selector in self.selectors:
            if (selector.collide(x, y)):
                return selector
        return None

    def on_click(self, x: int, y: int) -> None:
        button = self.get_button_at(x, y)
        if button:
            button.execute()

        selector = self.get_selector_at(x, y)
        if selector:
            print("Color selector clicked")
            pixel_color = self.image.get_pixel(x, y)
            selector.execute(pixel_color)
