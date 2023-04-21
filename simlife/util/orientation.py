import simlife.util.direction as direction


class _North:
    def to_direction(self):
        return direction.Direction(0, -1)


class _South:
    def to_direction(self):
        return direction.Direction(0, 1)


class _East:
    def to_direction(self):
        return direction.Direction(1, 0)


class _West:
    def to_direction(self):
        return direction.Direction(-1, 0)


NORTH = _North()
EAST = _East()
SOUTH = _South()
WEST = _West()
