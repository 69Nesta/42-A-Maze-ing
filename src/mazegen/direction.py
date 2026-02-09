from enum import Enum


class Direction(Enum):
    """Cardinal directions used to reference walls.

    Members:
        NORTH(0): top wall.
        EAST(1): right wall.
        SOUTH(2): bottom wall.
        WEST(3): left wall.
    """

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
