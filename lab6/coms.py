from random import randrange
from math import sqrt, radians, sin, cos
import pygame
from GraphComs import *


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
    Class that has all parameters of current game session in it

    Walls -- list with all consisting walls of Wall class in it
    pool -- list with all consisting ball of Ball class in it
    score -- score of current game
    highscore -- the highest score in the current session
    MaxspeedChanging -- variable that can be -1, 0, 1 and helps to control the
        speed of the balls in the pool
    '''
    Walls = []
    pool = []
    score = 0
    highscore = -1
    MaxspeedChanging = 0
    username = 'admin'

    def __init__(self, Maxspeed, Xmax, Ymax, Quantity, radius,
                 FPS = 90, WIDTH = 1100, HEIGHT = 700):
        '''
        Defining start parameters of the session:

        WIDTH, HEIGHT -- parameters of the main window
        BoxWIDTH, BoxHEIGHT -- parameters of the game zone
        Maxspeed -- speed of the balls
        Xmax, Ymax -- maximal module of the coordinates of the balls
        Quantity, radius -- balls' parameters
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

        for i in range(self.Quantity):
            self.pool.append(Ball(self.Maxspeed,
                                  self.Xmax, self.Ymax,
                                  -self.Xmax, -self.Ymax))
        
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

        if int(open('data.txt', 'r').read().split()[0]) < self.highscore:
            with open('data.txt', 'w') as f:
                f.write(str(int(self.highscore)) + ' by ' + self.username)
        

    def update(self):
        '''
        Updates position of the balls, checks collisions, changes the speed of
        the balls
        '''
        for i in self.pool:

            for j in self.Walls:
                i.try_collision(j)
                
            i.move()

            i.clocktickes()

        if abs(self.MaxspeedChanging):
            OldMaxspeed = self.Maxspeed
            
            self.Maxspeed += self.MaxspeedChanging * 0.05
            if self.Maxspeed <= 0:
                self.Maxspeed = 0.05

            for i in self.pool:
                i.speedx *= self.Maxspeed/OldMaxspeed
                i.speedy *= self.Maxspeed/OldMaxspeed
        
    def get_event(self, event):
        '''
        Works with events
        '''
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
        
