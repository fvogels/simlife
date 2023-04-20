class Direction:
    def __init__(self, dx, dy):
        self.__dx = dx
        self.__dy = dy

    @property
    def dx(self):
        return self.__dx

    @property
    def dy(self):
        return self.__dy

    def __repr__(self):
        return f'Direction({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        dx = self.dx + other.dx
        dy = self.dy + other.dy
        return Direction(dx, dy)

    def __bool__(self):
        return bool(self.dx) or bool(self.dy)


NORTH = Direction(0, -1)
EAST = Direction(1, 0)
SOUTH = Direction(0, 1)
WEST = Direction(-1, 0)
CENTER = Direction(0, 0)