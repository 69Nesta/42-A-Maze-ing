from .types import t_point


class Coords:
    """(x, y) coordinate pair.

    Args:
        x (int): X coordinate (column).
        y (int): Y coordinate (row).
    """

    def __init__(self, x: int, y: int):
        """Initialize a Coords instance with x and y values.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            None
        """
        self.x: int = x
        self.y: int = y

    def to_tuple(self) -> t_point:
        """Return the coordinate pair as a tuple.

        Returns:
            t_point: A tuple (x, y) representing this coordinate.
        """
        return (self.x, self.y)

    @classmethod
    def from_tuple(cls, coords: t_point) -> 'Coords':
        """Create a Coords instance from a (x, y) tuple.

        Args:
            coords (t_point): A tuple containing (x, y).

        Returns:
            Coords: A new Coords instance constructed from the tuple.
        """
        x, y = coords
        return cls(x, y)
