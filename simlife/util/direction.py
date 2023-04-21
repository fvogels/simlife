from .orientation import *


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
        return f'Direction({self.dx}, {self.dy})'

    def __str__(self):
        return f'({self.dx}, {self.dy})'

    def __add__(self, other):
        dx = self.dx + other.dx
        dy = self.dy + other.dy
        return Direction(dx, dy)

    def __bool__(self):
        return bool(self.dx) or bool(self.dy)

    def rotate(self, orientation):
        if orientation is NORTH:
            return self
        if orientation is SOUTH:
            return Direction(-self.dx, -self.dy)
        if orientation is EAST:
            return Direction(-self.dy, self.dx)
        if orientation is WEST:
            return Direction(self.dy, -self.dx)
        raise RuntimeError('Invalid orientation')

    def __eq__(self, other):
        if isinstance(other, Direction):
            return self.dx == other.dx and self.dy == other.dy
        else:
            return NotImplemented
