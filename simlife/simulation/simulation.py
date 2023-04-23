from simlife.simulation.entities import *


class Simulation:
    def __init__(self, world):
        self.__world = world

    @property
    def world(self):
        return self.__world

    def compute_next(self):
        boids = [cell for cell in self.__world if isinstance(cell, Boid)]
        for boid in boids:
            boid.energy -= 1
            decision = boid.decide_action()
            self.__process_rotation(boid, decision)
            self.__process_movement(boid, decision)
            self.__process_fight(boid, decision)
            self.__process_death(boid)

    def __process_rotation(self, boid, decision):
        if boid.energy > 0:
            boid.orientation = boid.orientation.rotate(decision.rotation)
            boid.energy -= 1

    def __process_movement(self, boid, decision):
        if boid.energy > 0 and decision.movement_direction:
            energy_consumed = abs(decision.movement_direction.dx) + abs(decision.movement_direction.dy)
            boid.energy -= energy_consumed
            old_position = boid.position
            new_position = old_position + decision.movement_direction.rotate(boid.orientation)
            if self.__world.is_valid_position(new_position) and self.__world[new_position] is None:
                self.__world.move_entity(old_position, new_position)

    def __process_fight(self, boid, decision):
        if decision.fight:
            boid.energy -= 1
            enemy_position = boid.position + boid.orientation.to_direction()
            if self.__world.is_valid_position(enemy_position):
                other_boid = self.__world[enemy_position]
                if isinstance(other_boid, Boid):
                    if boid.energy >= other_boid.energy:
                        winner = boid
                        loser = other_boid
                    else:
                        winner = other_boid
                        loser = boid
                    winner.energy += 10
                    loser.energy -= 20

    def __process_death(self, boid):
        if boid.energy == 0:
            self.__world.remove_entity(boid.position)