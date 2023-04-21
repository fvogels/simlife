import pytest
from simlife.util import *


@pytest.mark.parametrize('direction, orientation, expected', [
    (Direction(0, -1), NORTH, Direction(0, -1)),
    (Direction(0, -1), EAST, Direction(1, 0)),
    (Direction(0, -1), SOUTH, Direction(0, 1)),
    (Direction(0, -1), WEST, Direction(-1, 0)),
    (Direction(1, 0), NORTH, Direction(1, 0)),
    (Direction(1, 0), EAST, Direction(0, 1)),
    (Direction(1, 0), SOUTH, Direction(-1, 0)),
    (Direction(1, 0), WEST, Direction(0, -1)),
])
def test_rotation(direction, orientation, expected):
    actual = direction.rotate(orientation)

    assert expected == actual