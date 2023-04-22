from simlife.ann.neuralnetwork import *
from simlife.ann.neurons import *
from simlife.util.direction import *
from simlife.util.orientation import *


class ArtificialIntelligence:
    def __init__(self, *, neural_network_template, dna, boid):
        builder = NeuralNetworkBuilder()
        layers = neural_network_template(boid)
        self.__output_layer = layers[-1]

        connections = (
            (neuron1, neuron2)
            for layer1, layer2 in zip(layers, layers[1:])
            for neuron1 in layer1
            for neuron2 in layer2
        )
        for index, (input_neuron, output_neuron) in enumerate(connections):
            builder.connect(input_neuron, output_neuron, dna[index])
        self.__neural_network = builder.build()

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
