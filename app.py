import pygame
import sys
from simlife.simulation.world import World
from simlife.simulation import Simulation, Boid, ArtificialIntelligence
from simlife.util import *


FRAMES_PER_SECOND = 75
CELL_SIZE = 8
WINDOW_SIZE = (128 * CELL_SIZE, 128 * CELL_SIZE)

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)


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


world = World(128, 128)
ai = ArtificialIntelligence()
world.add_entity(Boid(world, Position(0, 0), EAST, ai))
simulation = Simulation(world)

simulation_timer = Timer(0.5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    display_surface.fill((0,0,0))

    render_world(display_surface, simulation.world)

    pygame.display.flip()

    elapsed_seconds = clock.tick(FRAMES_PER_SECOND) / 1000
    if simulation_timer.tick(elapsed_seconds):
        simulation.compute_next()
