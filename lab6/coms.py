from random import randrange
from math import sqrt, radians, sin, cos
import pygame
from GraphComs import trans, distance
from Colors import YELLOW, OLIVE, WHITE, GRAY, RED, KINOVAR, BLACK


class Ball:
    '''
    Class of the Ball, which has it's coordinates, speed and can collide with
    walls (class Wall) without losing energy

    time_from_colliding is time from last colliding with a wall
    '''

    time_from_colliding = 11

    def __init__(self, speedmax, xmax, ymax, xmin=0, ymin=0):
        '''
        Generating speed along x- and y- axes (speedx, speedy) and x- and y-
        coordinates (x, y)

        speedmax -- maximal speed along one axis (in fact the speed of the ball)
        xmax, ymax -- maximal x- and y- coordinates of the ball
        xmin, ymin -- minimal x- and y- coordinates of the ball
        '''

        self.speedx = randrange(int(speedmax * 2 * 100 + 1)) / 100 - speedmax
        self.speedy = randrange(-1, 2, 2) * sqrt(speedmax ** 2 - self.speedx ** 2)
        
        self.x = randrange(int((xmax - xmin - speedmax) * 100)) / 100 + xmin + speedmax/2
        self.y = randrange(int((ymax - ymin - speedmax) * 100)) / 100 + ymin + speedmax/2
        
    def move(self):
        '''
        Changes the ball's coordinate on each iteration due to it's speed
        '''
        self.x += self.speedx
        self.y += self.speedy

    def try_collision(self, AWall):
        '''
        Checks colliding with the wall object AWall and due to it changes the
        ball's speed along axes
        '''
        if self.time_from_colliding >= 0:
            if AWall.orintation == 0:
                if abs(AWall.y0 - self.y) <= abs((self.speedy)):
                    self.speedy = - self.speedy
                    self.y += self.speedy * 1.01
                    self.timefromcolliding = 0

            if AWall.orintation == 90:
                if abs(AWall.x0 - self.x) <= abs((self.speedx)):
                    self.speedx = - self.speedx
                    self.x += self.speedx * 1.01
                    self.timefromcolliding = 0

    def clocktickes(self):
        '''
        Counts iterations from last colliding with a wall
        '''
        self.time_from_colliding += 1


class Wall:
    '''
    Class of static wall, with which can collide balls
    '''

    def __init__(self, x0, y0, x1, y1, ori):
        '''
        Gives to the wall it's parameters:
        
        x0, y0 -- coordinates of one end-point of the wall
        x1, y1 -- coordinates of another end-point of the wall
        orintation (ori) -- angle between the wall and vertical axis
        '''
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.orintation = ori
        
    def coords(self):
        '''
        Returns two-dimensional list of wall's end-points' coordinates
        '''
        return [[self.x0, self.y0], [self.x1, self.y1]]

class Game:
    '''
    Class that has all parameters of current game session in it.
    It manages the game, makes the window. where it is launched and draws actions

    Walls -- list with all consisting walls of Wall class in it
    pool -- list with all consisting ball of Ball class in it
    score -- score of current game
    highscore -- the highest score in the current session
    MaxspeedChanging -- variable that can be -1, 0, 1 and helps to control the
        speed of the balls in the pool
    username -- name of current player to be written in the all-time highscore
        line. In the current moment cannot be changed by user, it is a
        preparation for a future feature
    '''
    Walls = []
    pool = []
    score = 0
    highscore = -1
    MaxspeedChanging = 0
    username = 'admin'
    logged = False

    def __init__(self, Maxspeed, Xmax, Ymax, Quantity, radius,
                 FPS = 90, WIDTH = 1100, HEIGHT = 700, game_length = 15):
        '''
        Defining start parameters of the session:

        WIDTH, HEIGHT -- parameters of the main window
        BoxWIDTH, BoxHEIGHT -- parameters of the game zone
        Maxspeed -- speed of the balls
        Xmax, Ymax -- maximal module of the coordinates of the balls
        Quantity, radius -- balls' parameters
        game_length -- time length of one game (in seconds)
        time -- game's personal clock; how many frames is remaining before new
            round will start
        sc -- screen, where everything is happening
        '''
        self.BoxWIDTH = WIDTH // 2
        self.BoxHEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.FPS = FPS
        self.Maxspeed = Maxspeed
        self.Xmax = Xmax
        self.Ymax = Ymax
        self.Quantity = Quantity
        self.radius = radius
        self.game_length = game_length

        self.time = game_length * FPS
        self.sc = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.login()
        self.restart()  # Refreshing session's data

    def restart(self):
        '''
        Launching a new game in the session by making new balls' positions,
        updating highscore and all-time highscore
        '''
        self.Walls = []
        self.pool = []
        self.highscore = max(self.highscore, self.score)
        self.score = 0

        # Defining balls
        
        for i in range(self.Quantity):
            self.pool.append(Ball(self.Maxspeed,
                                  self.Xmax, self.Ymax,
                                  -self.Xmax, -self.Ymax))

        # Defining walls
        
        self.Walls.append(Wall(self.Xmax, self.Ymax,
                          self.Xmax, -self.Ymax,
                          90))  # right wall
        self.Walls.append(Wall(-self.Xmax, self.Ymax,
                          -self.Xmax, -self.Ymax,
                          90))  # left wall
        self.Walls.append(Wall(-self.Xmax, -self.Ymax,
                          self.Xmax, -self.Ymax,
                          0))  # bottom wall
        self.Walls.append(Wall(-self.Xmax, self.Ymax,
                          self.Xmax, self.Ymax,
                          0))  # top wall

        # Updating all-time highscore
        
        if int(open('data.txt', 'r').read().split()[0]) < self.highscore:
            with open('data.txt', 'w') as f:
                f.write(str(int(self.highscore)) + ' by ' + self.username)
        

    def update(self):
        '''
        Updating situation and parameters
        '''
        if self.time <= 0:  # checks if current round is finished
            self.time = self.game_length * self.FPS
            self.restart()

        self.time -= 1

        self.draw()  # draws all on the screen
        
        for i in self.pool:  # updates balls' positions and checks collisions

            for j in self.Walls:
                i.try_collision(j)
                
            i.move()

            i.clocktickes()

        if abs(self.MaxspeedChanging):  # checks if user changed balls' speed
            OldMaxspeed = self.Maxspeed
            
            self.Maxspeed += self.MaxspeedChanging * 0.05
            if self.Maxspeed <= 0:
                self.Maxspeed = 0.05

            for i in self.pool:
                i.speedx *= self.Maxspeed/OldMaxspeed
                i.speedy *= self.Maxspeed/OldMaxspeed

        for i in pygame.event.get():  # catches application's events
            self.get_event(i)
        
    def get_event(self, event):
        '''
        Works with events
        '''
        if self.logged:
            if event.type == pygame.QUIT:
                exit()  # Quits
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.restart()  # Launchs new game
                    
                elif event.key == pygame.K_UP:
                    self.radius += 1  # Makes balls bigger
                elif event.key == pygame.K_DOWN:
                    if self.radius >= 2:
                        self.radius -= 1  # Makes balls smaller, but not with
                                          # zero radius
                elif event.key == pygame.K_w:
                    self.MaxspeedChanging = 1  # Makes balls faster
                elif event.key == pygame.K_s:
                    self.MaxspeedChanging = -1  # Makes balls slower
                    
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    self.MaxspeedChanging = 0  # Stops changing balls' speed
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # checks catching a ball
                    position = event.pos
                    
                    for i, ball in enumerate(self.pool):
                        if distance(position,
                                    trans(self.HEIGHT, self.WIDTH,
                                          self.BoxHEIGHT, self.BoxWIDTH,
                                          (ball.x, ball.y))) <= self.radius:
                            self.score += ((ball.speedx**2 + ball.speedy**2)**0.5
                                           /self.radius*1000)
                            self.pool[i] = Ball(self.Maxspeed,
                                                self.Xmax, self.Ymax,
                                                -self.Xmax, -self.Ymax)
        else:
            if event.type == pygame.QUIT:
                exit()  # Quits
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == 13:  # Enter button
                    self.logged = True
                elif 97 <= event.key <= 122:
                    letters = 'abcdefghijklmnopqrstuvwxyz'
                    self.username += letters[event.key - 97]
                elif 48 <= event.key <= 57:
                    self.username += str(event.key - 48)
                        
    def draw(self):
        '''
        Draws all on the screen
        '''
        self.sc.fill(GRAY())

        #Writing necessary signs in the left part of the game window

        ScoreText = pygame.font.Font(None, 128).render('Score: '
                                                       + str(int(self.score)),
                                                       True, YELLOW())
        self.sc.blit(ScoreText, (10, 50))

        HighScoreText = pygame.font.Font(None, 72).render('Highcore: '
                                                          + str(int(self.highscore)),
                                                       True, OLIVE())
        self.sc.blit(HighScoreText, (10, 200))

        AllTimeHighScoreText = pygame.font.Font(None, 36).render('All-time Highcore: '
                                                          + open('data.txt', 'r').read(),
                                                                 True, OLIVE())
        self.sc.blit(AllTimeHighScoreText, (120, 20))
        
        SpeedText = pygame.font.Font(None, 72).render('Balls speed: '
                                                      + str(int(self.Maxspeed*20)),
                                                       True, WHITE())
        self.sc.blit(SpeedText, (10, 350))

        ChangeSpeedText = pygame.font.Font(None, 36).render('To change use W and S buttons',
                                                      True, WHITE())
        self.sc.blit(ChangeSpeedText, (10, 405))

        RadiusText = pygame.font.Font(None, 96).render('Balls radius: '
                                                       + str(self.radius),
                                                       True, WHITE())
        self.sc.blit(RadiusText, (10, 500))

        ChangeRadiusText = pygame.font.Font(None, 36).render('To change use UP and DOWN arrows',
                                                       True, WHITE())
        self.sc.blit(ChangeRadiusText, (10, 571))

        TimeText = pygame.font.Font(None, 72).render(str(self.time//self.FPS),
                                                     True, RED())
        self.sc.blit(TimeText, (10, 10))

        #Drawing the balls and the walls

        for i in self.pool:
            pygame.draw.circle(self.sc, KINOVAR(), (trans(self.HEIGHT, self.WIDTH,
                                                     self.BoxHEIGHT, self.BoxWIDTH,
                                                     [i.x, i.y])), self.radius)

        for i in self.Walls:
            Coordins = [trans(self.HEIGHT, self.WIDTH,
                              self.BoxHEIGHT, self.BoxWIDTH, j)
                        for j in i.coords()]
            pygame.draw.line(self.sc, BLACK(), Coordins[0], Coordins[1])

    def login(self):

        while not self.logged:
            self.sc.fill(GRAY())

            LogText = pygame.font.Font(None, 72).render('Enter your name: '
                                                        + self.username,
                                                         True, WHITE())
            self.sc.blit(LogText, (10, 10))


            for i in pygame.event.get():  # catches application's events
                self.get_event(i)

            pygame.display.update()
