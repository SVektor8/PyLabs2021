import pygame as pg
from pygame.draw import rect, ellipse

def alpha_ellipse(length, width, x, y):
    global Surfaces, colors, sc

    Surfaces.append(pg.Surface(f(length, width), pg.SRCALPHA))
    ellipse(Surfaces[-1], colors[7], f(0, 0, length, width))
    sc.blit(Surfaces[-1], f(x, y))

def sun_alpha_ellipse(length, width, x, y):
    global Surfaces, colors, sc

    Surfaces.append(pg.Surface(f(length, width), pg.SRCALPHA))
    ellipse(Surfaces[-1], colors[13], f(0, 0, length, width))
    sc.blit(Surfaces[-1], f(x, y))

def f(*args): 
    k = 2
    
    return [i // k for i in args]

def fr(*args):
    k = 2
    mas = [i for i in args]
    
    mas[2] -= mas[0]
    mas[3] -= mas[1]

    return [i // k for i in mas]

def frc(q, *args):
    k = 2
    mas = [i for i in args]

    mas[2] -= mas[0]
    mas[3] -= mas[1]
    mas[0] += 75

    return [round(q * i / k )for i in mas]

def car(sc, x, y, size, color): # size = length, x & y of the top left border
    global colors

    q = size/335

    Surfaces.append(pg.Surface(f(round(q*348), round(q*114)), pg.SRCALPHA))

    ellipse(Surfaces[-1], colors[8], frc(q, -75, 75, -49, 83))
    
    rect(Surfaces[-1], color, frc(q, 0, 0, 165, 35))
    rect(Surfaces[-1], color, frc(q, -62, 35, 272, 94))

    rect(Surfaces[-1], colors[6], frc(q, 13, 8, 66, 38))
    rect(Surfaces[-1], colors[6], frc(q, 98, 6, 148, 35))

    ellipse(Surfaces[-1], colors[8], frc(q, -36, 66, 29, 112))
    ellipse(Surfaces[-1], colors[8], frc(q, 190, 66, 254, 112))

    sc.blit(Surfaces[-1], f(x - 75, y))

colors = [( 83, 108, 103),
          (183, 196, 200),
          (147, 167, 172),
          (183, 200, 196),
          (147, 172, 167),
          (111, 145, 138),
          (219, 227, 226),
          (147, 172, 167, 144),
          #(190, 204, 202, 128),
          (  0,  34,  23),
          (  0, 204, 255),
          (100,  36,  36),   #red
          (149,  95,  32),   #yellow
          (  1,  93,  82),   #green
          #(255, 146,  24, 16)
          (204,  85,   0, 4)]

Surfaces = []

pg.init()



sc = pg.display.set_mode(f(794, 1123)) # screen

rect(sc, (255, 255, 255), fr(0, 708, 794, 714)) # background
rect(sc, colors[1], fr(0, 0, 794, 708))
rect(sc, colors[0], fr(0, 714, 794, 1123))
ellipse(sc, colors[3], fr(-179, 933, 1109, 1869))


for i in range(20, 200, 2):
    sun_alpha_ellipse(2*i, 2*i, 520 - i, 80 - i)

alpha_ellipse(842, 176, -388, 502)

rect(sc, colors[2], fr(16, 21, 178, 737)) 
rect(sc, colors[4], fr(206, 57, 373, 751))

alpha_ellipse(842, 176, -279, 58)

rect(sc, colors[3], fr(126, 161, 313, 848))
rect(sc, colors[6], fr(597, 21, 778, 746))
rect(sc, colors[5], fr(526, 198, 697, 864))

alpha_ellipse(842, 176, 231, -20)
alpha_ellipse(842, 176, 166, 276)

alpha_ellipse(220, 60, 52, 884)
alpha_ellipse(220, 60, -107, 808)
alpha_ellipse(220, 60, 58, 957)

car(sc, 465, 740, 90, colors[12])

car(sc, 500, 830, 150, colors[9])
car(sc, 100, 830, 150, colors[9])

car(sc, 330, 850, 200, colors[11])

car(sc, 590, 877, 270, colors[10])
    
car(sc, 372, 930, 335, colors[9])


pg.display.update()
