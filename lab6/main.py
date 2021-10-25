import pygame
from coms import Ball, Wall, Game
from GraphComs import trans
from Colors import YELLOW, OLIVE, WHITE, GRAY, RED, KINOVAR, BLACK

# Parameters of the screen and the "Box" -- zone, where the game is launched
# Xmax, Ymax -- maximal coordinats if the system, which (0, 0) is in the center
# of the "Box"
# game length -- time length of one game (in seconds)

FPS = 60
WIDTH = 1100
HEIGHT = 700
BoxWIDTH = WIDTH // 2
BoxHEIGHT = HEIGHT
Xmax = BoxWIDTH / 2
Ymax = BoxHEIGHT / 2
game_length = 15

# Default parameters of the balls

Quantity = 10
Maxspeed = 1
radius = 10

# Initialisation of the screen (sc) and pygame clock

pygame.init()
clock = pygame.time.Clock()

# GG is the Game object, which has all the information about the current game

GG = Game(Maxspeed, Xmax, Ymax, Quantity, radius,
          FPS, WIDTH, HEIGHT, game_length)

while 1:
    # Updating display and the game situation

    GG.update()

    pygame.display.update()

    clock.tick(FPS)
