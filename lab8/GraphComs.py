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
