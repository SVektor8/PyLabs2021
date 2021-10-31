from coms import GameMaster
import pygame


FPS = 30

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


clock = pygame.time.Clock()

GG = GameMaster(screen)

while not GG.finished:
    GG.update()

    clock.tick(FPS)

pygame.quit()
