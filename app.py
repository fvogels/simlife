from itertools import pairwise
import pygame
import random
import sys
from simlife.ann.neuralnetwork import NeuralNetworkBuilder
from simlife.simulation.ai import ArtificialIntelligence
from simlife.simulation.state import State
from simlife.ann.neurons import *
from simlife.simulation import *
from simlife.util import *


FRAMES_PER_SECOND = 75
CELL_SIZE = 8
WINDOW_SIZE = (128 * CELL_SIZE, 128 * CELL_SIZE)

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)


class HardcodedPhenotypeBuilder:
    def build(self, boid, dna):
        builder = NeuralNetworkBuilder()
        builder.connect(LatitudeSensor(boid), step := StepNeuron(0.2, 1, 0), 1)
        builder.connect(step, output1 := HorizontalMovementDecisionNeuron(relative=False), 1)
        builder.connect(AroundSensor(boid), output2 := VerticalMovementDecisionNeuron(relative=False), 1)
        neural_network = builder.build()
        return ArtificialIntelligence(neural_network, [output1, output2])


class PhenotypeBuilder:
    def build(self, boid, dna):
        genes = iter(dna)

        layers = [
            [
                ConstantNeuron(1.0),
                AroundSensor(boid),
                # HorizontalOrientationSensor(boid),
                # VerticalOrientationSensor(boid),
                LatitudeSensor(boid),
                # LongitudeSensor(boid),
                EnergySensor(boid),
            ],
            [
                IdentityNeuron(),
                IdentityNeuron(),
                IdentityNeuron(),
                StepNeuron(next(genes), next(genes), next(genes)),
                StepNeuron(next(genes), next(genes), next(genes)),
                StepNeuron(next(genes), next(genes), next(genes)),
                StepNeuron(next(genes), next(genes), next(genes)),
                StepNeuron(next(genes), next(genes), next(genes)),
                StepNeuron(next(genes), next(genes), next(genes)),
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


def render_world(surface, world):
    for y in range(world.height):
        for x in range(world.width):
            position = Position(x, y)
            entity = world.entity_at(position)
            rectangle = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if isinstance(entity, Boid):
                color = RED
            elif isinstance(entity, Wall):
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


def fitness_metric(boid):
    return boid.position.x


def survival_predicate(boid):
    return boid.position.x >= 100


state = State(
    fitness_metric=fitness_metric,
    survival_predicate=survival_predicate ,
    phenotype_builder=PhenotypeBuilder(),
    mutation_rate=1,
    boid_initial_energy=100,
    auto_steps_per_generation=100,
    simulation_rules=[
        AbsoluteMotionRule(),
        DeathRule(),
    ],
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
