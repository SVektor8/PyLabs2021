import math


def distance(pos1, pos2):
    """
    Calculates distance between two dots

        Args:
            pos1: Tuple with x- and y- coordinates of the dot
            pos2: Tuple with x- and y- coordinates of the dot
        Returns:
            Returns distance between dots (type: float)
    """
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def turn(coo, angle):
    """
    Turns radius-vector of a dot in coordinate system on an angle and returns
    a tuple with new coordinates

        Args:
            coo: tuple with start coordinates
            angle: angle to turn the vector
        Returns:
            tuple with new coordinates
    """
    x, y = coo[0], coo[1]

    r = (x ** 2 + y ** 2) ** 0.5

    if x != 0:
        angle = math.atan(y / x) + angle
    else:
        angle = math.pi / 2 - (y < 0) * math.pi + angle

    if (x < 0) * (y < 0) \
            or (x < 0) * (y > 0):  # third and second quarters
        angle = angle - math.pi

    x, y = r * math.cos(angle), r * math.sin(angle)

    return (x, y)
