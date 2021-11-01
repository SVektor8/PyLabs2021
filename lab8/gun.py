import pygame
from coms import GameMaster

# Game parameters

FPS = 30

WIDTH = 800
HEIGHT = 600

# Initialization of pygame and screen

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Initialization of the game

GG = GameMaster(screen)

while not GG.finished:
    # updating game situation

    GG.update()

    clock.tick(FPS)

pygame.quit()
