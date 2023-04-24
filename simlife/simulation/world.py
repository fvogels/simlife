import random
from simlife.util import Grid, Position
from simlife.util.orientation import *
from simlife.simulation.entities import Boid


class World:
    def __init__(self, width, height):
        self.__grid = Grid(width, height, lambda p: Cell())

    @property
    def width(self):
        return self.__grid.width

    @property
    def height(self):
        return self.__grid.height

    @property
    def entities(self):
        for y in range(self.height):
            for x in range(self.width):
                position = Position(x, y)
                entity = self.__grid[position].entity
                if entity:
                    yield entity

    def entity_at(self, position):
        return self.__grid[position].entity

    def add_boid(self, *, dna, phenotype_builder, position=None, orientation=None, energy=None):
        position = position or self.__create_random_unused_position()
        orientation = orientation or self.__create_random_orientation()
        boid = Boid(world=self, position=position, orientation=orientation, dna=dna, phenotype_builder=phenotype_builder, energy=energy)
        self.__grid[position].entity = boid

    def add_entity(self, position, entity):
        self.__grid[position].entity = entity

    def move_entity(self, origin, destination):
        assert self.is_valid_position(origin)
        assert self.is_valid_position(destination)
        assert self.__grid[origin].entity is not None
        assert self.__grid[destination].entity is None
        entity = self.__grid[origin].entity
        self.__grid[origin].entity = None
        self.__grid[destination].entity = entity
        entity.position = destination

    def remove_entity(self, position):
        self[position].entity = None

    def is_valid_position(self, position):
        return self.__grid.is_valid_position(position)

    def __create_random_unused_position(self):
        while True:
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
            position = Position(x, y)
            if self.is_empty(position):
                return position

    def __create_random_orientation(self):
        return random.choice([
            NORTH,
            EAST,
            SOUTH,
            WEST
        ])

    def is_empty(self, position):
        return self.is_valid_position(position) and self.__grid[position].entity is None


class Cell:
    def __init__(self):
        self.entity = None
        self.pheromone = 0
