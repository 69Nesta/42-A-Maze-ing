from src.direction import Direction


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = {
            Direction.NORTH: True,
            Direction.EAST: True,
            Direction.SOUTH: True,
            Direction.WEST: True,
        }

    def remove_wall(self, direction: Direction):
        self.walls[direction] = False

    def has_wall(self, direction: Direction) -> bool:
        return self.walls[direction]

    def is_full(self):
        return self.walls[Direction.NORTH] and \
               self.walls[Direction.EAST] and \
               self.walls[Direction.SOUTH] and \
               self.walls[Direction.WEST]

    def export(self) -> str:
        bits = [
            int(self.walls[Direction.WEST]),
            int(self.walls[Direction.SOUTH]),
            int(self.walls[Direction.EAST]),
            int(self.walls[Direction.NORTH]),
        ]
        bit_str = ''.join(str(b) for b in bits)
        hex_value = hex(int(bit_str, 2))[2:].upper()
        return hex_value

    def import_cell(self, data: str):
        if data.isdigit():
            bits = f"{int(data):04b}"
        else:
            bits = f"{int(data, 16):04b}"
        self.walls[Direction.NORTH] = bits[3] == '1'
        self.walls[Direction.EAST] = bits[2] == '1'
        self.walls[Direction.SOUTH] = bits[1] == '1'
        self.walls[Direction.WEST] = bits[0] == '1'
