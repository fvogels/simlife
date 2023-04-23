import pytest
from simlife.ann.neurons import *
from simlife.util.position import *
from simlife.util.orientation import *


class WorldStub:
    def __init__(self, *, width=128, height=128):
        self.width = width
        self.height = height

class BoidStub:
    def __init__(self, *, position=None, orientation=None, world=None):
        self.position = position or Position(0, 0)
        self.orientation = orientation or NORTH
        self.world = world or WorldStub()



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


@pytest.mark.parametrize('orientation, expected', [
    (NORTH, -1.0),
    (SOUTH, 1.0),
    (EAST, 0.0),
    (WEST, 0.0),
])
def test_vertical_orientation_sensor(orientation, expected):
    boid = BoidStub(orientation=orientation)
    neuron = VerticalOrientationSensor(boid)
    assert neuron.determine_output() == expected


@pytest.mark.parametrize('width, x, y, expected', [
    *(
        (128, 0, y, -1.0)
        for y in range(0, 128)
    ),
    *(
        (128, 127, y, 1.0)
        for y in range(0, 128)
    ),
    (11, 5, 0, 0.0),
])
def test_latitude_sensor(width, x, y, expected):
    world = WorldStub(width=width)
    boid = BoidStub(position=Position(x, y), world=world)
    neuron = LatitudeSensor(boid)
    assert neuron.determine_output() == expected


@pytest.mark.parametrize('height, x, y, expected', [
    *(
        (128, x, 0, -1.0)
        for x in range(0, 128)
    ),
    *(
        (128, x, 127, 1.0)
        for x in range(0, 128)
    ),
    (11, 0, 5, 0.0),
])
def test_longitude_sensor(height, x, y, expected):
    world = WorldStub(height=height)
    boid = BoidStub(position=Position(x, y), world=world)
    neuron = LongitudeSensor(boid)
    assert neuron.determine_output() == expected
