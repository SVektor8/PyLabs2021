import math


def trans(Height, Width, BoxHeight, BoxWidth, coords):
    '''
    Function transforms coordinats from one system to another, which is bounded
    with the main window of the program
    
    Height -- Height of the window
    Width -- Width of the window
    BoxHeight -- Height of the zone, where the game is launched
    BoxWidth -- Width of the zone, where the game is launched
    coords -- turple or list of two numbers, first is the x-coordinate in system
        of the zone, where the game is launched, second is the y-coordinate there
        (0, 0) is in the center of the zone
    '''
    x0 = coords[0]
    y0 = coords[1]
    return int(Width + x0 - BoxWidth / 2), int(Height - BoxHeight / 2 - y0)


def distance(pos1, pos2):
    '''
    Returns distance between two dots

    pos1, pos2 -- turples, each of two numbers, first number in each turple is
        x-coordinate of the dot, second number -- y-coordinate
    '''
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def turn(coo, angle):
    x, y = coo[0], coo[1]

    r = (x ** 2 + y ** 2) ** 0.5

    if x != 0:
        angle = math.atan(y / x) + angle
    else:
        angle = math.pi / 2 - (y < 0) * math.pi + angle

    if (x < 0) * (y < 0) \
            or (x / abs(x) == -1) * (y / abs(y) == 1):
        angle = angle - math.pi

    x, y = r * math.cos(angle), r * math.sin(angle)

    return (x, y)
