from simlife.ann.neuralnetwork import *
from simlife.ann.neurons import *
from simlife.util.direction import *
from simlife.util.orientation import *


class ArtificialIntelligence:
    def __init__(self, dna, boid):
        builder = NeuralNetworkBuilder()
        input_layer = [
            ConstantNeuron(1.0),
            FrontSensor(boid),
            HorizontalOrientationSensor(boid),
            VerticalOrientationSensor(boid),
            LatitudeSensor(boid),
            LongitudeSensor(boid),
        ]
        intermediate_layer = [
            MemoryNeuron(),
            MemoryNeuron(),
            MemoryNeuron(),
            MemoryNeuron(),
        ]
        self.__output_layer = [
            HorizontalMovementDecisionNeuron(),
            VerticalMovementDecisionNeuron(),
            RotationDecisionNeuron(),
        ]

        connections = [
            *(
                (i, o)
                for i in input_layer
                for o in intermediate_layer
            ),
            *(
                (i, o)
                for i in intermediate_layer
                for o in self.__output_layer
            )
        ]
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
