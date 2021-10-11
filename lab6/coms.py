import random
from math import sqrt, radians, sin, cos


class Corpuscula:
    speedx = 0
    speedy = 0
    x = 0
    y = 0

    timefromcolliding = 11

    def __init__(self, speedmax, xmax, ymax, xmin=0, ymin=0):



        k = random.randrange(2)
        if k == 1:
            self.speedx = (random.randrange((speedmax + 1) * 2 * 100) / 100 - speedmax) % speedmax
        else:
            self.speedx = -((random.randrange((speedmax + 1) * 2 * 100) / 100 - speedmax) % speedmax)
        k = random.randrange(2)
        if k == 1:
            self.speedy = sqrt(speedmax ** 2 - self.speedx ** 2)
        else:
            self.speedy = -sqrt(speedmax ** 2 - self.speedx ** 2)

        self.x = random.randrange((xmax - xmin - speedmax ) * 100) / 100 + xmin + speedmax/2
        self.y = random.randrange((ymax - ymin - speedmax) * 100) / 100 + ymin + speedmax/2

    def defcoo(self, xx, yy):
        self.x = xx
        self.y = yy

    def defspe(self, sx, sy):
        self.speedx = sx
        self.speedy = sy

    def move(self):
        self.x += self.speedx
        self.y += self.speedy

    def trycolli(self, AWall):
        if self.timefromcolliding >= 0:
            if AWall.orintation == 0:
                if abs(AWall.y0 - self.y) <= abs((self.speedy - AWall.speed)):
                    self.speedy = - self.speedy + 2 * AWall.Speedy()
                    self.y += self.speedy*1.01
                    self.timefromcolliding = 0

            if AWall.orintation == 90:
                if abs(AWall.x0 - self.x) <= abs((self.speedx - AWall.speed)):
                    self.speedx = - self.speedx + 2 * AWall.Speedx()
                    self.x += self.speedx*1.01
                    self.timefromcolliding = 0

    def clocktickes(self):
        self.timefromcolliding+=1


class Wall:
    moving = False
    x0 = 0
    x1 = 0
    y0 = 0
    y1 = 0
    orintation = -1
    speed = 0

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

    def Speedx(self):
        return self.speed * sin(radians(self.orintation))

    def Speedy(self):
        return self.speed * cos(radians(self.orintation))

    def CanMove(self):
        self.moving = True
