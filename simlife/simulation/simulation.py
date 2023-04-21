class Simulation:
    def __init__(self, world):
        self.__world = world

    @property
    def world(self):
        return self.__world

    def compute_next(self):
        boids = [cell for cell in self.__world if cell is not None]
        for boid in boids:
            decision = boid.decide_action()
            boid.orientation = boid.orientation.rotate(decision.rotation)
            if decision.movement_direction:
                old_position = boid.position
                new_position = old_position + decision.movement_direction.rotate(boid.orientation)
                if self.__world.is_valid_position(new_position) and self.__world[new_position] is None:
                    self.__world.move_entity(old_position, new_position)
