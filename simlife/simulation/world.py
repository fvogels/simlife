from simlife.util import Grid, Position, Direction


class World:
    def __init__(self, width, height):
        self.__grid = Grid(width, height, lambda p: None)

    @property
    def width(self):
        return self.__grid.width

    @property
    def height(self):
        return self.__grid.height

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                position = Position(x, y)
                yield self.__grid[position]

    def __getitem__(self, position):
        return self.__grid[position]

    def __setitem__(self, position, value):
        self.__grid[position] = value

    def add_entity(self, entity):
        self[entity.position] = entity

    def move_entity(self, origin, destination):
        assert self.is_valid_position(origin)
        assert self.is_valid_position(destination)
        assert self[origin] is not None
        assert self[destination] is None
        entity = self[origin]
        self[origin] = None
        self[destination] = entity
        entity.position = destination

    def is_valid_position(self, position):
        return self.__grid.is_valid_position(position)
