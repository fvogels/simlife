import pygame
import random
import sys
from simlife.simulation.world import World
from simlife.ann.neurons import *
from simlife.simulation import Simulation, Boid, Wall
from simlife.util import *
from simlife.simulation.dna import DNA


FRAMES_PER_SECOND = 75
CELL_SIZE = 8
WINDOW_SIZE = (128 * CELL_SIZE, 128 * CELL_SIZE)

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)


class State:
    def __init__(self, *, fitness_metric, survival_predicate):
        self.__fitness_metric = fitness_metric
        self.__survival_predicate = survival_predicate
        self.__template = self.__create_neural_network_template()
        self.__boid_count = 1000
        self.__simulation = self.__create_simulation(generate_dna=lambda: DNA.create_random(6 * 4 + 4 * 3))
        self.__runner = self.__runner_function()
        self.__generation = 0
        self.__mutation_rate = 10

    def __create_neural_network_template(self):
        def create(boid):
            input_layer = [
                ConstantNeuron(1.0),
                FrontSensor(boid),
                HorizontalOrientationSensor(boid),
                VerticalOrientationSensor(boid),
                LatitudeSensor(boid),
                LongitudeSensor(boid),
            ]
            intermediate_layer = [
                SigmoidNeuron(),
                SigmoidNeuron(),
                SigmoidNeuron(),
                SigmoidNeuron(),
            ]
            output_layer = [
                HorizontalMovementDecisionNeuron(),
                VerticalMovementDecisionNeuron(),
                RotationDecisionNeuron(),
            ]
            return (input_layer, intermediate_layer, output_layer)

        return create

    def __create_simulation(self, *, generate_dna):
        world = World(128, 128)
        for y in range(20, 108, 2):
            world.add_entity(Position(64, y), Wall())
        for _ in range(self.__boid_count):
            world.add_boid(dna=generate_dna(), neural_network_template=self.__template)
        return Simulation(world)

    def step(self):
        next(self.__runner)

    def __runner_function(self):
        while True:
            for _ in range(100):
                self.__simulation.compute_next()
                yield None
            self.__next_generation()

    def __next_generation(self):
        def generate_dna():
            dna1 = dnas[random_index()]
            dna2 = dnas[random_index()]
            dna = dna1.crossover(dna2)
            if random.randrange(0, self.__mutation_rate) == 0:
                dna = dna.mutate()
            return dna

        def random_index():
            x = random.random() ** 5
            return int(x * len(dnas))

        boids = (cell for cell in self.__simulation.world if isinstance(cell, Boid))
        survivors = sorted((boid for boid in boids if self.__survival_predicate(boid)), key=self.__fitness_metric, reverse=True)
        dnas = [boid.dna for boid in survivors]
        print(f'Survivors in generation {self.__generation}: {len(dnas)}')
        print(f'Winner: energy={survivors[0].energy} dna={survivors[0].dna}')
        self.__generation += 1
        self.__simulation = self.__create_simulation(generate_dna=generate_dna)

    @property
    def world(self):
        return self.__simulation.world


def render_world(surface, world):
    for y in range(world.height):
        for x in range(world.width):
            position = Position(x, y)
            cell = world[position]
            rectangle = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if isinstance(cell, Boid):
                color = RED
            elif isinstance(cell, Wall):
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(surface, color, rectangle)


# Initialize Pygame
pygame.init()

# Create window with given size
display_surface = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


state = State(
    fitness_metric=lambda boid: boid.position.x,
    survival_predicate=lambda boid: boid.position.x > 64
)
simulation_timer = Timer(0.001)
visual_timer = Timer(0.02)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    elapsed_seconds = clock.tick(FRAMES_PER_SECOND) / 1000
    if simulation_timer.tick(elapsed_seconds):
        state.step()

    if visual_timer.tick(elapsed_seconds):
        display_surface.fill((0,0,0))
        render_world(display_surface, state.world)
        pygame.display.flip()
