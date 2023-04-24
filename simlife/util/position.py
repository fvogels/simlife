class Position:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __repr__(self):
        return f'Position({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, direction):
        x = self.x + direction.dx
        y = self.y + direction.dy
        return Position(x, y)

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx ** 2 + dy ** 2) ** 0.5

    @property
    def around(self):
        x = self.x
        y = self.y
        yield Position(x - 1, y)
        yield Position(x, y - 1)
        yield Position(x + 1, y)
        yield Position(x, y + 1)
