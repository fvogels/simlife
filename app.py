import pygame
import sys


FRAMES_PER_SECOND = 75
WINDOW_SIZE = (500, 500)

# Initialize Pygame
pygame.init()

# Create window with given size
display_surface = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    display_surface.fill((0,0,0))
    pygame.display.flip()

    elapsed_seconds = clock.tick(FRAMES_PER_SECOND) / 1000
