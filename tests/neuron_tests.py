import pytest
from simlife.ann.neurons import *
from simlife.util.position import *
from simlife.util.orientation import *


class BoidStub:
    def __init__(self, *, position=None, orientation=None):
        self.position = position or Position(0, 0)
        self.orientation = orientation or NORTH



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
def test_sign_neuron(threshold, input, output):
    neuron = SignNeuron(threshold)
    neuron.feed_input(input)
    assert output == neuron.determine_output()


@pytest.mark.parametrize('orientation, expected', [
    (NORTH, 0.0),
    (SOUTH, 0.0),
    (EAST, 1.0),
    (WEST, -1.0),
])
def test_horizontal_orientation_sensor(orientation, expected):
    boid = BoidStub(orientation=orientation)
    neuron = HorizontalOrientationSensor(boid)
    assert neuron.determine_output() == expected
