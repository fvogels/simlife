from simlife.ann.neuralnetwork import *
from simlife.ann.neurons import *
from simlife.util.direction import *
from simlife.util.orientation import *


class ArtificialIntelligence:
    def __init__(self, dna, boid):
        def decider():
            decision = Decision()
            decision.movement_direction += horizontal_movement_neuron.determine_output()
            decision.movement_direction += vertical_movement_neuron.determine_output()
            return decision

        builder = NeuralNetworkBuilder()
        input_layer = [
            ConstantNeuron(1.0),
            FrontSensor(boid),
        ]
        output_layer = [
            horizontal_movement_neuron := ClassifierNeuron(negative_value=WEST.to_direction(), zero_value=Direction(0, 0), positive_value=EAST.to_direction()),
            vertical_movement_neuron := ClassifierNeuron(negative_value=NORTH.to_direction(), zero_value=Direction(0, 0), positive_value=SOUTH.to_direction())
        ]

        for index, (input_neuron, output_neuron) in enumerate((i, o) for i in input_layer for o in output_layer):
            builder.connect(input_neuron, output_neuron, dna[index])

        self.__neural_network = builder.build()
        self.__decider = decider

    def decide_action(self):
        self.__neural_network.update()
        return self.__decider()


def ai_factory(dna):
    return lambda boid: ArtificialIntelligence(dna, boid)

class Decision:
    def __init__(self):
        self.movement_direction = Direction(0, 0)
