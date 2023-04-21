import pygame
import random
import sys
from simlife.simulation.world import World
from simlife.simulation import Simulation
from simlife.util import *
from simlife.simulation.dna import DNA


FRAMES_PER_SECOND = 75
CELL_SIZE = 8
WINDOW_SIZE = (128 * CELL_SIZE, 128 * CELL_SIZE)

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)


class State:
    def __init__(self):
        self.__boid_count = 1000
        self.__simulation = self.__create_simulation(generate_dna=lambda: DNA.create_random(4))
        self.__runner = self.__runner_function()

    def __create_simulation(self, *, generate_dna):
        world = World(128, 128)
        for _ in range(self.__boid_count):
            world.add_boid(dna=generate_dna())
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
            dna1 = random.choice(dnas)
            dna2 = random.choice(dnas)
            return dna1.crossover(dna2)

        boids = (cell for cell in self.__simulation.world if cell is not None)
        survivors = (boid for boid in boids if boid.position.x > 64)
        dnas = [boid.dna for boid in survivors]
        print(f'Survivors: {len(dnas)}')
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
            if cell:
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(surface, color, rectangle)


# Initialize Pygame
pygame.init()

# Create window with given size
display_surface = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


state = State()
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

