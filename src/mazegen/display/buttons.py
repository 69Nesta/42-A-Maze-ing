"""UI helpers: buttons and selectors for maze display.

This module provides simple UI element classes used by the maze
display system: clickable buttons, a color selector, grouped
selector buttons and a manager to draw and route clicks to these
elements.
"""

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
                 callback: Callable[[], None] | None = None):
        """A simple rectangular button.

        Args:
            label: The text label displayed for the button.
            x: X coordinate of the button's top-left corner.
            y: Y coordinate of the button's top-left corner.
            width: Width of the button in pixels.
            height: Height of the button in pixels.
            background: Background color (packed int) used when drawing.
            text_color: Color used to render the label text.
            callback: Optional callable executed when the button is clicked.

        Returns:
            None
        """
        self.label: str = label
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.background: int = background
        self.text_color: int = text_color
        self.callback: Callable[[], None] | None = callback

    def execute(self) -> None:
        """Execute the button callback if one is set.

        Returns:
            None
        """

        if self.callback is not None:
            self.callback()

    def draw(self, image: Image) -> None:
        """Draw the button onto the provided image.

        Args:
            image: The target Image instance used for drawing.

        Returns:
            None
        """

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
                 callback: Callable[[int], None] | None = None):
        """A small color swatch used to pick colors from the image.

        The color selector draws a square and expects clicks inside that
        square; when clicked it reports the pixel color at the click
        location (as an int) to its callback.

        Args:
            label: Text label displayed alongside the selector.
            x: X coordinate of the selector's top-left corner.
            y: Y coordinate of the selector's top-left corner.
            size: Size (width and height) of the selector square in pixels.
            label_color: Color used to render the label text.
            callback: Optional callable that receives an int color when
                the selector is used.

        Returns:
            None
        """

        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.label: str = label
        self.label_color: int = label_color
        self.callback: Callable[[int], None] | None = callback
        self.offset_y: int = 20

    def collide(self, x: int, y: int) -> bool:
        """Return True if the given point collides with the selector square.

        Args:
            x: X coordinate of the point to test.
            y: Y coordinate of the point to test.

        Returns:
            True if (x, y) lies inside the selector square, otherwise False.
        """

        offset_y = self.offset_y
        return (self.x <= x <= self.x + self.size - 1 and
                self.y + offset_y <= y <= self.y + offset_y + self.size - 1)

    def execute(self, color: int) -> None:
        """Call the selector callback with the chosen color.

        Args:
            color: The selected color (packed int) to deliver to the callback.

        Returns:
            None
        """

        if self.callback is not None:
            self.callback(color)

    def draw(self, image: Image) -> None:
        """Draw the color selector square on the provided image.

        Args:
            image: The Image instance to draw onto.

        Returns:
            None
        """

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
                callback: Callable[[int], None] | None = None
            ) -> None:
        """A single selectable button used within a Selector group.

        Args:
            label: Text label for the button.
            x: X coordinate of the button's top-left corner.
            y: Y coordinate of the button's top-left corner.
            width: Width of the button in pixels.
            height: Height of the button in pixels.
            background: Background color when not selected.
            selected_background: Inner background color used when selected.
            border_color: Border color used to indicate selection.
            text_color: Color used to render the button label.
            callback: Optional callable receiving the selected index when
                this button is activated.

        Returns:
            None
        """

        self.label: str = label
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.background: int = background
        self.selected_background: int = selected_background
        self.border_color: int = border_color
        self.text_color: int = text_color
        self.callback: Callable[[int], None] | None = callback

    def execute(self, index: int) -> None:
        """Call the button's callback with the provided index.

        Args:
            index: The integer index representing this button within a group.

        Returns:
            None
        """

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
        """Draw this selector button onto the provided image.

        Args:
            image: Image instance used for drawing.
            selected: If True, draw the button in its selected state.

        Returns:
            None
        """

    def collide(self, x: int, y: int) -> bool:
        """Return True if the point (x, y) is inside this button.

        Args:
            x: X coordinate of the point to test.
            y: Y coordinate of the point to test.

        Returns:
            True if the point collides with the button rectangle.
        """

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
                callback: Callable[[int], None] | None = None
            ) -> None:
        """A group of selectable `SelectorButton`s with a shared label.

        The Selector maintains the current selected index and routes clicks
        to the appropriate button callbacks.

        Args:
            image: Image instance used to draw the selector buttons.
            label: Label text displayed above the group.
            x: X coordinate for the selector group's origin.
            y: Y coordinate for the selector group's origin.
            choice: List of SelectorButton instances that belong to this group.
            default_index: The initially selected index in the choice list.
            text_color: Color used to render the label text.
            callback: Optional callable receiving the new index when selection
                changes.

        Returns:
            None
        """

        self.image: Image = image
        self.label: str = label
        self.x: int = x
        self.y: int = y
        self.choice: list[SelectorButton] = choice
        self.current_index: int = default_index
        self.text_color: int = text_color
        self.callback: Callable[[int], None] | None = callback

    def execute(self, index: int) -> None:
        """Invoke the selector-level callback with the provided index.

        Args:
            index: Newly selected index.

        Returns:
            None
        """

        if self.callback is not None:
            self.callback(index)

    def draw(self) -> None:
        """Draw all choice buttons and mark the image as needing update.

        Returns:
            None
        """

        for i, button in enumerate(self.choice):
            selected = (i == self.current_index)
            button.draw(self.image, selected)
        self.image.need_update = True

    def on_click(self, x: int, y: int) -> None:
        """Handle a click at (x, y), update selection if a button was hit.

        Args:
            x: X coordinate of the click.
            y: Y coordinate of the click.

        Returns:
            None
        """

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
        """Manage and render multiple UI elements and their text labels.

        The ButtonManager stores buttons, color selectors and selector
        groups, draws them onto the provided image and routes click events
        to the appropriate element.

        Args:
            image: Image instance used for drawing elements.
            offset_x: Horizontal offset applied to label placement.
            text_manager: TextManager used to create and manage labels.

        Returns:
            None
        """

        self.image = image
        self.buttons: list[Button] = []
        self.color_selectors: list[ColorSelector] = []
        self.selectors: list[Selector] = []
        self.offset_x = offset_x
        self.texts = text_manager

    def draw_buttons(self) -> None:
        """Draw all registered buttons, color selectors and selectors.

        Returns:
            None
        """

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

        """Register a Button and create its text label.

        Args:
            id: Identifier used by the TextManager for the label.
            button: Button instance to register and draw.

        Returns:
            None
        """

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
        """Register a ColorSelector and create its text label.

        Args:
            id: Identifier used by the TextManager for the label.
            selector: ColorSelector instance to register and draw.

        Returns:
            None
        """

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
        """Register a Selector group and create its labels.

        Args:
            id: Identifier used by the TextManager for the group label.
            selector: Selector instance to register and draw.

        Returns:
            None
        """

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
        """Return the Button at the given point, or None if none match.

        Args:
            x: X coordinate of the point to test.
            y: Y coordinate of the point to test.

        Returns:
            The Button instance that contains the point, or None.
        """

        for button in self.buttons:
            if (button.x <= x <= button.x + button.width and
                    button.y <= y <= button.y + button.height):
                return button
        return None

    def get_color_selector_at(self, x: int, y: int) -> ColorSelector | None:
        """Return the ColorSelector at the given point, or None if none match.

        Args:
            x: X coordinate of the point to test.
            y: Y coordinate of the point to test.

        Returns:
            The ColorSelector instance that contains the point, or None.
        """

        for color_selector in self.color_selectors:
            if (color_selector.collide(x, y)):
                return color_selector
        return None

    def on_click(self, x: int, y: int) -> None:
        """Handle a click at (x, y), dispatching to the appropriate element.

        The dispatch order is: regular buttons, color selectors, then selector
        groups. If a color selector is activated, the pixel color at the click
        location is retrieved from the managed image and passed to the
        selector's callback.

        Args:
            x: X coordinate of the click.
            y: Y coordinate of the click.

        Returns:
            None
        """

        button = self.get_button_at(x, y)
        if button:
            button.execute()

        color_selector = self.get_color_selector_at(x, y)
        if color_selector:
            pixel_color = self.image.get_pixel(x, y)
            color_selector.execute(pixel_color)

        for selector in self.selectors:
            selector.on_click(x, y)
