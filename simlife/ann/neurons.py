class ConstantNeuron:
    def __init__(self, constant):
        self.__constant = constant

    def determine_output(self):
        return self.__constant


class FrontSensor:
    def __init__(self, boid):
        self.__boid = boid

    def determine_output(self):
        boid = self.__boid
        world = boid.world
        position_in_front_of_boid = boid.position + boid.direction
        return world[position_in_front_of_boid] is not None


class RoundingNeuron:
    def __init__(self, threshold=0.1):
        self.__threshold = threshold
        self.__last_value = 0

    def feed_input(self, value):
        self.__last_value = value

    def determine_output(self):
        if self.__last_value > self.__threshold:
            return 1.0
        elif self.__last_value < -self.__threshold:
            return -1.0
        else:
            return 0.0
