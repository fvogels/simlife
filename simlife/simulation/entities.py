from simlife.simulation.ai import ArtificialIntelligence


class Boid:
    def __init__(self, world, position, orientation, dna):
        self.__orientation = orientation
        self.__world = world
        self.__position = position
        self.__dna = dna
        self.__artificial_intelligence = ArtificialIntelligence(dna, self)
        self.energy = 0

    @property
    def dna(self):
        return self.__dna

    @property
    def world(self):
        return self.__world

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        self.__position = new_position

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, new_orientation):
        self.__orientation = new_orientation

    def decide_action(self):
        return self.__artificial_intelligence.decide_action()


class Wall:
    pass
