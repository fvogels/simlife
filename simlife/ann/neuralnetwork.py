class NeuralNetwork:
    def __init__(self, neurons, synapses):
        self.__neurons = neurons
        self.__synapses = synapses

    def update(self):
        table = [None] * len(self.__neurons)
        for synapse in self.__synapses:
            total = 0
            for input, weight in synapse.inputs:
                if table[input] is None:
                    table[input] = self.__neurons[input].determine_output()
                total += table[input] * weight
            self.__neurons[synapse.output].feed_input(total)


class Synapse:
    def __init__(self, inputs, output):
        assert len(inputs) != 0
        self.__inputs = inputs
        self.__output = output

    @property
    def inputs(self):
        return self.__inputs

    @property
    def output(self):
        return self.__output


class NeuralNetworkBuilder:
    def __init__(self):
        self.__neurons = []
        self.__neuron_id_to_index = {}
        self.__synapse_table = []

    def connect(self, origin, destination, weight):
        origin_index = self.__determine_neuron_index(origin)
        destination_index = self.__determine_neuron_index(destination)
        self.__synapse_table[destination_index].append((origin_index, weight))

    def __determine_neuron_index(self, neuron):
        if id(neuron) not in self.__neuron_id_to_index:
            index = len(self.__neurons)
            self.__neurons.append(neuron)
            self.__neuron_id_to_index[id(neuron)] = index
            self.__synapse_table.append([])
            return index
        else:
            return self.__neuron_id_to_index[id(neuron)]

    def build(self):
        def add(destination):
            nonlocal synapses_order, computed
            if destination not in computed:
                origins = self.__synapse_table[destination]
                for origin, _ in origins:
                    add(origin)
                if origins:
                    synapses_order.append(destination)
                computed.add(destination)

        synapses_order = []
        computed = set()
        for i in range(len(self.__neurons)):
            add(i)
        computation = [Synapse(self.__synapse_table[i], i) for i in synapses_order]
        return NeuralNetwork(self.__neurons, computation)
