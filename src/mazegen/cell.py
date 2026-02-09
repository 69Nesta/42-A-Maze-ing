from .direction import Direction


class Cell:
    """Representation of a single maze cell and its walls.

    Each Cell tracks its coordinates, wall presence for four
    directions, and a set of flags used by generation and logo
    generation.
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize a Cell at the given coordinates.

        Args:
            x (int): X coordinate (column) of the cell.
            y (int): Y coordinate (row) of the cell.

        Returns:
            None
        """
        self.x: int = x
        self.y: int = y
        self.is_logo: bool = False
        self.logo_blank: bool = False
        self.is_visited: bool = False
        self.is_next: bool = False
        self.is_undo_perfect: bool = False
        self.walls: dict[Direction, bool] = {
            Direction.NORTH: True,
            Direction.EAST: True,
            Direction.SOUTH: True,
            Direction.WEST: True,
        }

    def remove_wall(self, direction: Direction) -> None:
        """Remove the wall on the specified side of the cell.

        Args:
            direction (Direction): The wall direction to remove.

        Returns:
            None
        """
        self.walls[direction] = False

    def has_wall(self, direction: Direction) -> bool:
        """Check whether a wall exists on the specified side.

        Args:
            direction (Direction): Direction to check.

        Returns:
            bool: True if the wall exists, False otherwise.
        """
        return self.walls[direction]

    def is_full(self) -> bool:
        """Determine whether the cell has all four walls present.

        Returns:
            bool: True if all walls are present, False otherwise.
        """
        return (
            self.walls[Direction.NORTH]
            and self.walls[Direction.EAST]
            and self.walls[Direction.SOUTH]
            and self.walls[Direction.WEST]
        )

    def export(self) -> str:
        """
        Return a string  that represents the walls in a compact hexadecimal
        form used by the maze export/import

        Returns:
            str: Hexadecimal representation of the cell's walls.
        """
        bits = [
            int(self.walls[Direction.WEST]),
            int(self.walls[Direction.SOUTH]),
            int(self.walls[Direction.EAST]),
            int(self.walls[Direction.NORTH]),
        ]
        bit_str = ''.join(str(b) for b in bits)
        hex_value = hex(int(bit_str, 2))[2:].upper()
        return hex_value

    def import_cell(self, data: str) -> None:
        """Set the cell wall state from an exported string.

        Args:
            data (str): The string produced by export() describing the
                wall bits (either decimal or hex).

        Returns:
            None
        """
        if data.isdigit():
            bits = f"{int(data):04b}"
        else:
            bits = f"{int(data, 16):04b}"
        self.walls[Direction.NORTH] = bits[3] == '1'
        self.walls[Direction.EAST] = bits[2] == '1'
        self.walls[Direction.SOUTH] = bits[1] == '1'
        self.walls[Direction.WEST] = bits[0] == '1'

    def set(self, north: bool, east: bool,
            south: bool, west: bool) -> None:
        """Set all four wall flags at once.

        Args:
            north (bool): Presence of the north wall.
            east (bool): Presence of the east wall.
            south (bool): Presence of the south wall.
            west (bool): Presence of the west wall.

        Returns:
            None
        """
        self.walls[Direction.NORTH] = north
        self.walls[Direction.EAST] = east
        self.walls[Direction.SOUTH] = south
        self.walls[Direction.WEST] = west

    def del_north(self) -> None:
        """Remove the north wall of the cell.

        Returns:
            None
        """
        self.walls[Direction.NORTH] = False

    def del_east(self) -> None:
        """Remove the east wall of the cell.

        Returns:
            None
        """
        self.walls[Direction.EAST] = False

    def del_south(self) -> None:
        """Remove the south wall of the cell.

        Returns:
            None
        """
        self.walls[Direction.SOUTH] = False

    def del_west(self) -> None:
        """Remove the west wall of the cell.

        Returns:
            None
        """
        self.walls[Direction.WEST] = False
