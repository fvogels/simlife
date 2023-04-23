from simlife.ann.neuralnetwork import *
from simlife.ann.neurons import *
from simlife.util.direction import *
from simlife.util.orientation import *


class ArtificialIntelligence:
    def __init__(self, neural_network, output_layer):
        self.__neural_network = neural_network
        self.__output_layer = output_layer

    def decide_action(self):
        self.__neural_network.update()
        decision = Decision()
        for neuron in self.__output_layer:
            neuron.determine_output()(decision)
        return decision


class Decision:
    def __init__(self):
        self.movement_direction = Direction(0, 0)
        self.rotation = NORTH
