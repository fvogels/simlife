import simlife.util.direction as direction


class _Orientation:
    def __init__(self, index):
        self.__index = index

    def to_direction(self):
        return [
            direction.Direction(0, -1),
            direction.Direction(1, 0),
            direction.Direction(0, 1),
            direction.Direction(-1, 0),
        ][self.__index]

    def rotate(self, other):
        idx = (self.__index + other.__index) % 4
        return [NORTH, EAST, SOUTH, WEST][idx]


NORTH = _Orientation(0)
EAST = _Orientation(1)
SOUTH = _Orientation(2)
WEST = _Orientation(3)
