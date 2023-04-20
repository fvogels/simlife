from simlife.ann.neuralnetwork import *
from simlife.ann.neurons import *
from simlife.util.direction import *


class ArtificialIntelligence:
    def __init__(self):
        builder = NeuralNetworkBuilder()
        constant = ConstantNeuron(1.0)
        self.__horizontal_movement_neuron = SignNeuron(0.1)
        builder.connect(constant, self.__horizontal_movement_neuron, 1.0)
        self.__neural_network = builder.build()

    def decide_action(self):
        self.__neural_network.update()
        horizontal_movement_decision = self.__horizontal_movement_neuron.determine_output()
        if horizontal_movement_decision == 1.0:
            return Decision(movement_direction=EAST)
        elif horizontal_movement_decision == -1.0:
            return Decision(movement_direction=WEST)
        else:
            return Decision(movement_direction=CENTER)


class Decision:
    def __init__(self, *, movement_direction):
        self.__movement_direction = movement_direction

    @property
    def movement_direction(self):
        return self.__movement_direction
