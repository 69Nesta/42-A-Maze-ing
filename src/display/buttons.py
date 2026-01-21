from typing import Callable
from .image import Image
from .text_manager import TextManager


class Button:
    def __init__(self,
                 label: str,
                 x: int, y: int,
                 width: int, height: int,
                 background: int,
                 text_color: int,
                 callback: Callable | None = None):
        self.label: str = label
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.background: int = background
        self.text_color: int = text_color
        self.callback: Callable | None = callback

    def execute(self) -> None:
        if self.callback is not None:
            self.callback()

    def draw(self, image: Image) -> None:
        image.draw_rectangle(
            self.x, self.y,
            self.width, self.height,
            self.background
        )


class ColorSelector:
    def __init__(self,
                 label: str,
                 x: int, y: int,
                 size: int,
                 label_color: int,
                 callback: Callable | None = None):
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.label: str = label
        self.label_color: int = label_color
        self.callback: Callable | None = callback
        self.offset_y: int = 20

    def collide(self, x: int, y: int) -> bool:
        offset_y = self.offset_y
        return (self.x <= x <= self.x + self.size - 1 and
                self.y + offset_y <= y <= self.y + offset_y + self.size - 1)

    def execute(self, color: int) -> None:
        if self.callback is not None:
            self.callback(color)

    def draw(self, image: Image) -> None:
        image.draw_color_selector(
            self.x, self.y + self.offset_y,
            self.size)


class SelectorButton:
    def __init__(
                self,
                label: str,
                x: int, y: int,
                width: int, height: int,
                background: int,
                selected_background: int,
                border_color: int,
                text_color: int,
                callback: Callable | None = None
            ) -> None:
        self.label: str = label
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.background: int = background
        self.selected_background: int = selected_background
        self.border_color: int = border_color
        self.text_color: int = text_color
        self.callback: Callable | None = callback

    def execute(self, index: int) -> None:
        if self.callback is not None:
            self.callback(index)

    def draw(self, image: Image, selected: bool) -> None:
        border: int = 2
        image.draw_rectangle(
            self.x, self.y,
            self.width, self.height,
            self.background if not selected else self.border_color
        )
        if selected:
            image.draw_rectangle(
                self.x + border, self.y + border,
                self.width - 2 * border, self.height - 2 * border,
                self.selected_background
            )

    def collide(self, x: int, y: int) -> bool:
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)


class Selector:
    def __init__(
                self,
                image: Image,
                label: str,
                x: int, y: int,
                choice: list[SelectorButton],
                default_index: int,
                text_color: int,
                callback: Callable | None = None
            ) -> None:
        self.image: Image = image
        self.label: str = label
        self.x: int = x
        self.y: int = y
        self.choice: list[SelectorButton] = choice
        self.current_index: int = default_index
        self.text_color: int = text_color
        self.callback: Callable | None = callback

    def execute(self, index: int) -> None:
        if self.callback is not None:
            self.callback(index)

    def draw(self) -> None:
        for i, button in enumerate(self.choice):
            selected = (i == self.current_index)
            button.draw(self.image, selected)
        self.image.need_update = True

    def on_click(self, x: int, y: int) -> None:
        for i, button in enumerate(self.choice):
            if button.collide(x, y):
                if (i == self.current_index):
                    return
                self.current_index = i
                button.execute(i)
                self.execute(i)
                self.image.need_update = True
                break


class ButtonManager:
    def __init__(
            self,
            image: Image,
            offset_x: int,
            text_manager: TextManager
            ) -> None:
        self.image = image
        self.buttons: list[Button] = []
        self.color_selectors: list[ColorSelector] = []
        self.selectors: list[Selector] = []
        self.offset_x = offset_x
        self.texts = text_manager

    def draw_buttons(self) -> None:
        image: Image = self.image

        for button in self.buttons:
            button.draw(image)

        for color_selector in self.color_selectors:
            color_selector.draw(image)

        for selector in self.selectors:
            selector.draw()

    def add_button(self, id: str, button: Button) -> None:
        image = self.image
        self.buttons.append(button)

        x0 = button.x
        y0 = button.y - 5
        w = len(button.label) * 10
        h = 11

        button.draw(image)
        self.texts.create_text(
            id,
            self.offset_x + x0 + (button.width - w) // 2,
            y0 + ((button.height - h) // 2),
            button.text_color,
            button.label
        )

    def add_color_selector(self, id: str, selector: ColorSelector) -> None:
        image: Image = self.image
        self.color_selectors.append(selector)
        selector.draw(image)
        self.texts.create_text(
            id,
            self.offset_x + selector.x,
            selector.y - 5,
            selector.label_color,
            selector.label
        )

    def add_selector(self, id: str, selector: Selector) -> None:
        image: Image = self.image

        self.selectors.append(selector)
        selector.draw()

        self.texts.create_text(
            id,
            self.offset_x + selector.x,
            selector.y - 5,
            selector.text_color,
            selector.label
        )

        for index, button in enumerate(selector.choice):
            x0 = button.x
            y0 = button.y - 5
            w = len(button.label) * 10
            h = 11

            self.texts.create_text(
                f'{id}_{index}',
                self.offset_x + x0 + (button.width - w) // 2,
                y0 + ((button.height - h) // 2),
                button.text_color,
                button.label
            )
        image.need_update = True

    def get_button_at(self, x: int, y: int) -> Button | None:
        for button in self.buttons:
            if (button.x <= x <= button.x + button.width and
                    button.y <= y <= button.y + button.height):
                return button
        return None

    def get_color_selector_at(self, x: int, y: int) -> ColorSelector | None:
        for color_selector in self.color_selectors:
            if (color_selector.collide(x, y)):
                return color_selector
        return None

    def on_click(self, x: int, y: int) -> None:
        button = self.get_button_at(x, y)
        if button:
            button.execute()

        color_selector = self.get_color_selector_at(x, y)
        if color_selector:
            pixel_color = self.image.get_pixel(x, y)
            color_selector.execute(pixel_color)

        for selector in self.selectors:
            selector.on_click(x, y)
