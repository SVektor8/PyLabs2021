import random
from math import sqrt, radians, sin, cos
import pygame
from GraphComs import *


class Ball:

    timefromcolliding = 11

    def __init__(self, speedmax, xmax, ymax, xmin=0, ymin=0):



        k = random.randrange(2)  # rewrite in 1 line
        if k == 1:
            self.speedx = (random.randrange(int((speedmax + 1) * 2 * 100)) / 100 - speedmax) % speedmax
        else:
            self.speedx = -((random.randrange(int((speedmax + 1) * 2 * 100)) / 100 - speedmax) % speedmax)
        k = random.randrange(2)
        if k == 1:
            self.speedy = sqrt(speedmax ** 2 - self.speedx ** 2)
        else:
            self.speedy = -sqrt(speedmax ** 2 - self.speedx ** 2)

        self.x = random.randrange(int((xmax - xmin - speedmax ) * 100)) / 100 + xmin + speedmax/2
        self.y = random.randrange(int((ymax - ymin - speedmax) * 100)) / 100 + ymin + speedmax/2

    def move(self):
        self.x += self.speedx
        self.y += self.speedy

    def try_collision(self, AWall):
        if self.timefromcolliding >= 0:
            if AWall.orintation == 0:
                if abs(AWall.y0 - self.y) <= abs((self.speedy - AWall.speed)):
                    self.speedy = - self.speedy + 2 * AWall.speedy()
                    self.y += self.speedy*1.01
                    self.timefromcolliding = 0

            if AWall.orintation == 90:
                if abs(AWall.x0 - self.x) <= abs((self.speedx - AWall.speed)):
                    self.speedx = - self.speedx + 2 * AWall.speedx()
                    self.x += self.speedx*1.01
                    self.timefromcolliding = 0

    def clocktickes(self):
        self.timefromcolliding+=1


class Wall:
    moving = False

    def __init__(self, x00, y00, x11, y11, ori, sp):
        self.x0 = x00
        self.x1 = x11
        self.y0 = y00
        self.y1 = y11
        self.orintation = ori
        self.speed = sp

    def coords(self):
        return [[self.x0, self.y0], [self.x1, self.y1]]

    def move(self):
        if self.orintation != -1:
            self.x0 += self.speed * sin(radians(self.orintation))
            self.x1 += self.speed * sin(radians(self.orintation))
            self.y0 += self.speed * cos(radians(self.orintation))
            self.y1 += self.speed * cos(radians(self.orintation))

    def speedx(self):
        return self.speed * sin(radians(self.orintation))

    def speedy(self):
        return self.speed * cos(radians(self.orintation))

    def canMove(self):
        self.moving = True


class Game:
    Walls = []
    pool = []
    score = 0
    highscore = -1
    radius = 10
    MaxspeedChanging = 0

    def __init__(self, Maxspeed, Xmax, Ymax, Quantity, radius,
                 FPS = 90, WIDTH = 1100, HEIGHT = 700):

        self.BoxWIDTH = WIDTH // 2  # ширина
        self.BoxHEIGHT = HEIGHT  # высота
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.FPS = FPS
        self.Maxspeed = Maxspeed
        self.Xmax = Xmax
        self.Ymax = Ymax
        self.Quantity = Quantity
        self.radius = radius

        self.restart()

    def restart(self):
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
                          90, 0))  # right
        self.Walls.append(Wall(-self.Xmax, self.Ymax,
                          -self.Xmax, -self.Ymax,
                          90, 0))  # left
        self.Walls.append(Wall(-self.Xmax, -self.Ymax,
                          self.Xmax, -self.Ymax,
                          0, 0))  # down
        self.Walls.append(Wall(-self.Xmax, self.Ymax,
                          self.Xmax, self.Ymax,
                          0, 0))  # up

    def update(self):
        for i in self.pool:

            for j in self.Walls:
                i.try_collision(j)
                
            i.move()

            i.clocktickes()

        if abs(self.MaxspeedChanging):
            self.Maxspeed += self.MaxspeedChanging * 0.05
            if self.Maxspeed <= 0:
                self.Maxspeed = 0.05
        
    def get_event(self, event):
        
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.restart()
                
            elif event.key == pygame.K_UP:
                self.radius += 1
            elif event.key == pygame.K_DOWN:
                self.radius -= 1
                
            elif event.key == pygame.K_w:
                self.MaxspeedChanging = 1
            elif event.key == pygame.K_s:
                self.MaxspeedChanging = -1
                
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.Walls[1].speed = 0
            if event.key in [pygame.K_w, pygame.K_s]:
                self.MaxspeedChanging = 0
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                position = event.pos
                
                for i, ball in enumerate(self.pool):
                    if distance(position,
                                trans(self.HEIGHT, self.WIDTH,
                                      self.BoxHEIGHT, self.BoxWIDTH,
                                      (ball.x, ball.y))) <= self.radius:
                        self.score += int(self.Maxspeed/self.radius*1000)
                        self.pool[i] = Ball(self.Maxspeed,
                                            self.Xmax, self.Ymax,
                                            -self.Xmax, -self.Ymax)
        
