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

    def __getitem__(self, position):
        return self.__grid[position]
