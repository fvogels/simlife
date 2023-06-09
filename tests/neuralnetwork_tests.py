import pytest
from simlife.ann.neurons import *
from simlife.ann.neuralnetwork import *


@pytest.mark.parametrize('constant, threshold, weight, output', [
    *(
        (c, t, w, 1.0)
        for c in [0.2, 0.3, 0.5, 1.0]
        for t in [0.0, 0.1, 0.4]
        for w in [0.1, 0.4, 0.9, 2.0]
        if t < c * w
    ),
    *(
        (-c, t, w, -1.0)
        for c in [0.2, 0.3, 0.5, 1.0]
        for t in [0.0, 0.1, 0.4]
        for w in [0.1, 0.4, 0.9, 2.0]
        if t < c * w
    ),
    *(
        (c, t, w, 0.0)
        for c in [0.2, 0.3, 0.5, 1.0]
        for t in [0.0, 0.1, 0.4]
        for w in [0.1, 0.4, 0.9, 2.0]
        if t > c * w
    ),
])
def test_network_with_single_link(constant, threshold, weight, output):
    builder = NeuralNetworkBuilder()
    constant = ConstantNeuron(constant)
    sign = SignNeuron(threshold)
    builder.connect(constant, sign, weight)
    network = builder.build()

    network.update()

    assert sign.determine_output() == output


@pytest.mark.parametrize('constant1, constant2, threshold, weight1, weight2, output', [
    *(
        (c1, c2, t, w1, w2, 1.0)
        for c1 in [0.2, 0.3, 0.5, 1.0]
        for c2 in [0.2, 0.3, 0.5, 1.0]
        for t in [0.0, 0.1, 0.4]
        for w1 in [0.1, 0.4, 0.9, 2.0]
        for w2 in [0.1, 0.4, 0.9, 2.0]
        if t < c1 * w1 + c2 * w2
    ),
    *(
        (-c1, -c2, t, w1, w2, -1.0)
        for c1 in [0.2, 0.3, 0.5, 1.0]
        for c2 in [0.2, 0.3, 0.5, 1.0]
        for t in [0.0, 0.1, 0.4]
        for w1 in [0.1, 0.4, 0.9, 2.0]
        for w2 in [0.1, 0.4, 0.9, 2.0]
        if t < c1 * w1 + c2 * w2
    ),
])
def test_network_with_two_layers(constant1, constant2, threshold, weight1, weight2, output):
    builder = NeuralNetworkBuilder()
    constant1 = ConstantNeuron(constant1)
    constant2 = ConstantNeuron(constant2)
    sign = SignNeuron(threshold)
    builder.connect(constant1, sign, weight1)
    builder.connect(constant2, sign, weight2)
    network = builder.build()

    network.update()

    assert sign.determine_output() == output


@pytest.mark.parametrize('constant, threshold1, threshold2, weight1, weight2, output', [
    *(
        (c, t1, t2, w1, w2, 1.0)
        for c in [0.2, 0.3, 0.5, 1.0]
        for t1 in [0.0, 0.1, 0.4]
        for t2 in [0.0, 0.1, 0.4]
        for w1 in [0.1, 0.4, 0.9]
        for w2 in [0.1, 0.4, 0.9]
        if c * w1 > t1 and w2 > t2
    ),
    *(
        (c, t1, t2, w1, w2, 0.0)
        for c in [0.2, 0.3, 0.5, 1.0]
        for t1 in [0.0, 0.1, 0.4]
        for t2 in [0.0, 0.1, 0.4]
        for w1 in [0.1, 0.4, 0.9]
        for w2 in [0.1, 0.4, 0.9]
        if c * w1 < t1 and w2 > t2
    ),
    *(
        (c, t1, t2, w1, w2, 0.0)
        for c in [0.2, 0.3, 0.5, 1.0]
        for t1 in [0.0, 0.1, 0.4]
        for t2 in [0.0, 0.1, 0.4]
        for w1 in [0.1, 0.4, 0.9]
        for w2 in [0.1, 0.4, 0.9]
        if c * w1 > t1 and w2 < t2
    ),
])
def test_network_with_three_layers(constant, threshold1, threshold2, weight1, weight2, output):
    builder = NeuralNetworkBuilder()
    constant = ConstantNeuron(constant)
    sign1 = SignNeuron(threshold1)
    sign2 = SignNeuron(threshold2)
    builder.connect(constant, sign1, weight1)
    builder.connect(sign1, sign2, weight2)
    network = builder.build()

    network.update()

    assert sign2.determine_output() == output
