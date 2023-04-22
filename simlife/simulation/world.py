import random
from simlife.util import Grid, Position
from simlife.util.orientation import *
from simlife.simulation.entities import Boid

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

    def add_boid(self, *, dna, neural_network_template, position=None, orientation=None):
        position = position or self.__create_random_unsed_position()
        orientation = orientation or self.__create_random_orientation()
        boid = Boid(world=self, position=position, orientation=orientation, dna=dna, neural_network_template=neural_network_template)
        self.__grid[position] = boid

    def add_entity(self, position, entity):
        self[position] = entity

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

    def __create_random_unsed_position(self):
        while True:
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
            position = Position(x, y)
            if self[position] is None:
                return position

    def __create_random_orientation(self):
        return random.choice([
            NORTH,
            EAST,
            SOUTH,
            WEST
        ])
