import pytest
from simlife.ann.neurons import *



@pytest.mark.parametrize('constant', [0, 0.1, -0.5])
def test_constant(constant):
    neuron = ConstantNeuron(constant)
    assert constant == neuron.determine_output()


@pytest.mark.parametrize('threshold, input, output', [
    (0.1, 0.0, 0.0),
    (0.1, 0.2, 1.0),
    (0.1, -0.2, -1.0),
    (0.2, 0.1, 0.0),
    (0.2, -0.1, 0.0),
])
def test_rounding_neuron(threshold, input, output):
    neuron = SignNeuron(0.1)
    neuron.feed_input(input)
    assert output == neuron.determine_output()
