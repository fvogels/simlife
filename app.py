from itertools import pairwise
import pygame
import random
import sys
from simlife.ann.neuralnetwork import NeuralNetworkBuilder
from simlife.simulation.ai import ArtificialIntelligence
from simlife.simulation.world import World
from simlife.ann.neurons import *
from simlife.simulation import *
from simlife.util import *
from simlife.simulation.dna import DNA


FRAMES_PER_SECOND = 75
CELL_SIZE = 8
WINDOW_SIZE = (128 * CELL_SIZE, 128 * CELL_SIZE)

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)


class PhenotypeBuilder:
    def build(self, boid, dna):
        genes = iter(dna)

        layers = [
            [
                ConstantNeuron(1.0),
                FrontSensor(boid),
                # HorizontalOrientationSensor(boid),
                # VerticalOrientationSensor(boid),
                LatitudeSensor(boid),
                LongitudeSensor(boid),
                # EnergySensor(boid),
            ],
            # [
            #     StepNeuron(next(genes)),
            #     StepNeuron(next(genes)),
            #     StepNeuron(next(genes)),
            # ],
            # [
            #     StepNeuron(next(genes)),
            #     StepNeuron(next(genes)),
            #     StepNeuron(next(genes)),
            # ],
            # [
            #     StepNeuron(next(genes)),
            #     StepNeuron(next(genes)),
            #     StepNeuron(next(genes)),
            # ],
            [
                HorizontalMovementDecisionNeuron(relative=False),
                VerticalMovementDecisionNeuron(relative=False),
                # RotationDecisionNeuron(),
                # FightDecisionNeuron(),
            ]
        ]
        builder = NeuralNetworkBuilder()

        for layer1, layer2 in pairwise(layers):
            for neuron1 in layer1:
                for neuron2 in layer2:
                    builder.connect(neuron1, neuron2, next(genes))

        neural_network = builder.build()
        artificial_intelligence = ArtificialIntelligence(neural_network, layers[-1])

        return artificial_intelligence


class State:
    def __init__(self, *, fitness_metric, survival_predicate):
        self.__boid_count = 1000
        self.__fitness_metric = fitness_metric
        self.__survival_predicate = survival_predicate
        self.__phenotype_builder = PhenotypeBuilder()
        self.__generation = 0
        self.__mutation_rate = 10
        self.__simulation = self.__create_simulation()

        self.__world = self.__create_world(generate_dna=lambda: DNA())
        self.__runner = self.__create_automatic_runner(100)

    def __create_world(self, generate_dna):
        world = World(128, 128)
        for y in range(20, 108, 2):
            world.add_entity(Position(64, y), Wall())
        for _ in range(self.__boid_count):
            world.add_boid(dna=generate_dna(), phenotype_builder=self.__phenotype_builder)
        return world

    def set_manual(self):
        self.__runner = self.__create_manual_runner()

    def set_automatic(self):
        self.__runner = self.__create_automatic_runner(100)

    def __create_simulation(self):
        rules = [
            AbsoluteMotionRule(),
            DeathRule(),
        ]

        return Simulation(rules)

    def step(self):
        next(self.__runner)

    def __create_automatic_runner(self, steps_per_generation):
        def runner():
            while True:
                for _ in range(steps_per_generation):
                    self.__simulation.compute_next(self.__world)
                    yield None
                self.next_generation()
        return runner()

    def __create_manual_runner(self):
        def runner():
            while True:
                self.__simulation.compute_next(self.__world)
                yield None

        return runner()

    def next_generation(self):
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

        boids = (cell for cell in self.__world if isinstance(cell, Boid))
        survivors = sorted((boid for boid in boids if self.__survival_predicate(boid)), key=self.__fitness_metric, reverse=True)
        dnas = [boid.dna for boid in survivors]
        print(f'Survivors in generation {self.__generation}: {len(dnas)}')
        print(f'Winner: energy={survivors[0].energy} dna={survivors[0].dna}')
        self.__generation += 1
        self.__world = self.__create_world(generate_dna=generate_dna)

    @property
    def world(self):
        return self.__world


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

# state = State(
#     fitness_metric=lambda boid: boid.energy,
#     survival_predicate=lambda boid: True
# )

# state = State(
#     fitness_metric=lambda boid: max(boid.position.x, 127-boid.position.x),
#     survival_predicate=lambda boid: boid.position.x > 117 or boid.position.x < 10
# )

state = State(
    fitness_metric=lambda boid: boid.position.x,
    survival_predicate=lambda boid: boid.position.x >= 100
)

simulation_timer = Timer(0.02)
visual_timer = Timer(0.02)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state.next_generation()
            elif event.key == pygame.K_a:
                print('Setting automatic mode')
                state.set_automatic()
            elif event.key == pygame.K_m:
                print('Setting manual mode')
                state.set_manual()

    elapsed_seconds = clock.tick(FRAMES_PER_SECOND) / 1000
    if simulation_timer.tick(elapsed_seconds):
        state.step()

    if visual_timer.tick(elapsed_seconds):
        display_surface.fill((0,0,0))
        render_world(display_surface, state.world)
        pygame.display.flip()
