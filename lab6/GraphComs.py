def trans(Height, Width, BoxHeight, BoxWidth, coords):  # преобразование для интерпретатора из удобной
    x0 = coords[0]
    y0 = coords[1]
    return int(Width + x0 - BoxWidth / 2), int(Height - BoxHeight / 2 - y0)

def distance(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
