import pygame
from coms import Ball, Wall, Game
from GraphComs import trans
from Colors import YELLOW, OLIVE, WHITE, GRAY, RED, KINOVAR, BLACK

#Parameters of the screen and the "Box" -- zone, where the game is launched
#Xmax, Ymax -- maximal coordinats if the system, which (0, 0) is in the center
#of the "Box"
#game length -- time length of one game (in seconds)

FPS = 60
WIDTH = 1100  
HEIGHT = 700  
BoxWIDTH = WIDTH // 2  
BoxHEIGHT = HEIGHT  
Xmax = BoxWIDTH / 2
Ymax = BoxHEIGHT / 2
game_length = 15

#Default parameters of the balls

Quantity = 10
Maxspeed = 1
radius = 10

# Initialisation of the screen (sc), pygame clock and variable that counts
# iterations (time)

time = game_length * FPS

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#GG is the Game object, which has all the information about the current game

GG = Game(Maxspeed, Xmax, Ymax, Quantity, radius, FPS, WIDTH, HEIGHT)

while 1:
    sc.fill(GRAY())

    if time <= 0:
        time = game_length * FPS
        GG.restart()

    time -= 1

    #Writing necessary signs in thye left part of the game window

    ScoreText = pygame.font.Font(None, 128).render('Score: ' + str(int(GG.score)),
                                                   True, YELLOW())
    sc.blit(ScoreText, (10, 50))

    HighScoreText = pygame.font.Font(None, 72).render('Highcore: '
                                                      + str(int(GG.highscore)),
                                                   True, OLIVE())
    sc.blit(HighScoreText, (10, 200))

    AllTimeHighScoreText = pygame.font.Font(None, 36).render('All-time Highcore: '
                                                      + open('data.txt', 'r').read(),
                                                             True, OLIVE())
    sc.blit(AllTimeHighScoreText, (120, 20))
    
    SpeedText = pygame.font.Font(None, 72).render('Balls speed: '
                                                  + str(int(GG.Maxspeed*20)),
                                                   True, WHITE())
    sc.blit(SpeedText, (10, 350))

    RadiusText = pygame.font.Font(None, 96).render('Balls radius: '
                                                   + str(GG.radius),
                                                   True, WHITE())
    sc.blit(RadiusText, (10, 500))

    TimeText = pygame.font.Font(None, 72).render(str(time//FPS), True, RED())
    sc.blit(TimeText, (10, 10))

    #Drawing the balls and the walls

    for i in GG.pool:
        pygame.draw.circle(sc, KINOVAR(), (trans(HEIGHT, WIDTH,
                                                 BoxHEIGHT, BoxWIDTH,
                                                 [i.x, i.y])), GG.radius)

    for i in GG.Walls:
        Coordins = [trans(HEIGHT, WIDTH, BoxHEIGHT, BoxWIDTH, j) for j in i.coords()]
        pygame.draw.line(sc, BLACK(), Coordins[0], Coordins[1])

    #Updating display and positions of the balls
    
    pygame.display.update()

    GG.update()
    
    #Catching events and working with them

    for i in pygame.event.get():
        GG.get_event(i)

    clock.tick(FPS)
