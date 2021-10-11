import pygame
from coms import *
from GraphComs import *
from Colors import *


FPS = 90
WIDTH = 1100  # ширина экрана
HEIGHT = 700  # высота экрана
BoxWIDTH = WIDTH // 2  # ширина
BoxHEIGHT = HEIGHT  # высота

Quantity = 10
Maxspeed = 1
Xmax = BoxWIDTH / 2
Ymax = BoxHEIGHT / 2

elspeed = 2
betspeed = 4
time = 0
radius = 10


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

GG = Game(Maxspeed, Xmax, Ymax, Quantity, radius, FPS, WIDTH, HEIGHT)

while 1:
    sc.fill(GRAY())

    time += 1

    ScoreText = pygame.font.Font(None, 128).render('Score: ' + str(GG.score),
                                                   True, YELLOW())
    sc.blit(ScoreText, (10, 50))

    HighScoreText = pygame.font.Font(None, 72).render('Highcore: ' + str(GG.highscore),
                                                   True, OLIVE())
    sc.blit(HighScoreText, (10, 200))
    
    SpeedText = pygame.font.Font(None, 72).render('Balls speed: ' + str(int(GG.Maxspeed*100)),
                                                   True, WHITE())
    sc.blit(SpeedText, (10, 350))

    RadiusText = pygame.font.Font(None, 96).render('Balls radius: ' + str(GG.radius),
                                                   True, WHITE())
    sc.blit(RadiusText, (10, 500))

    for i in GG.pool:
        pygame.draw.circle(sc, KINOVAR(), (trans(HEIGHT, WIDTH,
                                                 BoxHEIGHT, BoxWIDTH,
                                                 [i.x, i.y])), GG.radius)

    for i in GG.Walls:
        Coordins = [trans(HEIGHT, WIDTH, BoxHEIGHT, BoxWIDTH, j) for j in i.coords()]
        pygame.draw.line(sc, BLACK(), Coordins[0], Coordins[1])
        
    pygame.display.update()

    GG.update()

    for i in pygame.event.get():
        GG.get_event(i)

    clock.tick(FPS)
