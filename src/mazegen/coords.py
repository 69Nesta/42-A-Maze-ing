from .types import t_point


class Coords:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def to_tuple(self) -> t_point:
        return (self.x, self.y)

    @classmethod
    def from_tuple(cls, coords: t_point) -> 'Coords':
        x, y = coords
        return cls(x, y)
