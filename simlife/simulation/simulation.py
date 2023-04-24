from simlife.simulation.entities import *


class Simulation:
    def __init__(self, rules):
        self.__rules = rules

    def compute_next(self, world):
        # Strict evaluation is important here, otherwise boids will be added as they are processed
        world.spread_pheromones()
        boids = [entity for entity in world.entities if isinstance(entity, Boid)]

        for boid in boids:
            for rule in self.__rules:
                decision = boid.decide_action()
                rule.apply(boid, decision)

    def __process_fight(self, boid, decision):
        if decision.fight:
            boid.energy -= 1
            enemy_position = boid.position + boid.orientation.to_direction()
            if self.__world.is_valid_position(enemy_position):
                other_boid = self.entity_at[enemy_position]
                if isinstance(other_boid, Boid):
                    if boid.energy >= other_boid.energy:
                        winner = boid
                        loser = other_boid
                    else:
                        winner = other_boid
                        loser = boid
                    winner.energy += 10
                    loser.energy -= 20


class TimeDepletesEnergyRule:
    def apply(self, boid, decision):
        boid.energy -= 1


class MovementCostFunctions:
    @staticmethod
    def zero(direction):
        return 0

    @staticmethod
    def manhattan(direction):
        return abs(direction.dx) + abs(direction.dy)

    @staticmethod
    def single(direction):
        if direction:
            return 1
        else:
            return 0


class RelativeMotionRule:
    def __init__(self, movement_cost_function=None):
        self.__movement_cost_function = movement_cost_function or MovementCostFunctions.manhattan

    def apply(self, boid, decision):
        movement = decision.relative_motion.rotate(boid.orientation)
        if movement:
            energy_consumed = self.__movement_cost_function(movement)
            if boid.energy >= energy_consumed:
                world = boid.world
                boid.energy -= energy_consumed
                old_position = boid.position
                new_position = old_position + movement
                if world.is_empty(new_position):
                    world.move_entity(old_position, new_position)


class AbsoluteMotionRule:
    def __init__(self, movement_cost_function=None):
        self.__movement_cost_function = movement_cost_function or MovementCostFunctions.manhattan

    def apply(self, boid, decision):
        movement = decision.absolute_motion
        if movement:
            energy_consumed = self.__movement_cost_function(movement)
            if boid.energy >= energy_consumed:
                world = boid.world
                boid.energy -= energy_consumed
                old_position = boid.position
                new_position = old_position + movement
                if world.is_empty(new_position):
                    world.move_entity(old_position, new_position)


class RotationRule:
    def apply(self, boid, decision):
        if boid.energy > 0:
            boid.orientation = boid.orientation.rotate(decision.rotation)
            boid.energy -= 1


class DeathRule:
    def apply(self, boid, decision):
        if boid.energy <= 0:
            boid.world.remove_entity(boid.position)


class PheromoneRule:
    def __init__(self, energy_cost):
        self.__energy_cost = energy_cost

    def apply(self, boid, decision):
        if decision.release_pheromones:
            boid.world.update_pheromones(boid.position, 0.1)
            boid.energy -= self.__energy_cost