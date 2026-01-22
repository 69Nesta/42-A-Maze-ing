"""Text rendering utilities used by the maze display.

This module contains a lightweight `Text` container and a `TextManager`
that tracks named text items and renders them into an MLX window using
`mlx_string_put`.
"""

from typing import Any
from mlx import Mlx  # type: ignore[import-untyped]


class Text:
    def __init__(self, x: int, y: int, color: int, content: str) -> None:
        """Simple container storing a single text label.

        Args:
            x: X coordinate where the text will be rendered.
            y: Y coordinate where the text will be rendered.
            color: Packed integer color used when drawing the text.
            content: The text string to render.

        Returns:
            None
        """

        self.x: int = x
        self.y: int = y
        self.color: int = color
        self.content: str = content
        self.need_update: bool = True


class TextManager:
    def __init__(self, mlx: Mlx, mlx_ptr: Any, win_ptr: Any) -> None:
        """Manage multiple named text labels and render them via MLX.

        Args:
            mlx: The MLX binding/module used to perform string drawing.
            mlx_ptr: MLX context pointer used by MLX drawing functions.
            win_ptr: MLX window pointer where text will be drawn.

        Returns:
            None
        """

        self.mlx: Mlx = mlx
        self.mlx_ptr: Any = mlx_ptr
        self.win_ptr: Any = win_ptr
        self.texts: dict[str, Text] = {}
        self.need_update: bool = True

    def text_exists(self, id: str) -> bool:
        """Return True if a text entry with the given id exists.

        Args:
            id: Identifier of the text entry to check.

        Returns:
            True if the id exists, False otherwise.
        """

        for text_id in self.texts.keys():
            if text_id == id:
                return True
        return False

    def create_text(self, id: str, x: int, y: int, color: int, content: str
                    ) -> Text | None:
        """Create and register a new named text entry.

        If an entry with the same id already exists this function returns
        None and does not overwrite the existing entry.

        Args:
            id: Unique identifier for the text entry.
            x: X coordinate for rendering.
            y: Y coordinate for rendering.
            color: Packed integer color used for the text.
            content: The text content to render.

        Returns:
            The created Text object if successful, or None if the id
            already exists.
        """

        if self.text_exists(id):
            return None
        text: Text = Text(x, y, color, content)
        self.texts[id] = text
        self.need_update = True
        return text

    def put_texts_in(self, x: int, y: int, w: int, h: int) -> None:
        """Render all text entries whose coordinates fall within the
        specified rectangle.

        Args:
            x: X coordinate of the rectangle's top-left corner.
            y: Y coordinate of the rectangle's top-left corner.
            w: Width of the rectangle.
            h: Height of the rectangle.

        Returns:
            None
        """

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
        """Render all texts that need updating, or all texts if `force`.

        Args:
            force: If True, render every text regardless of its
                `need_update` flag.

        Returns:
            None
        """

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
        """Return whether any text needs updating.

        Args:
            force: If True, inspect individual Text.need_update flags and
                return True if any are set. If False, return the
                TextManager's aggregated `need_update` flag.

        Returns:
            True if texts need updating according to the chosen policy,
            False otherwise.
        """

        if force:
            for text in self.texts.values():
                if text.need_update:
                    return True
            return False
        else:
            return self.need_update

    def update_text(self, id: str, new_content: str
                    ) -> bool:
        """Update the content of a named text entry.

        Args:
            id: Identifier of the text entry to update.
            new_content: New string content to assign.

        Returns:
            True if the update succeeded, False if the id was not found.
        """

        for text_id, text in self.texts.items():
            if text_id == id:
                text.content = new_content
                text.need_update = True
                self.need_update = True
                return True
        return False
