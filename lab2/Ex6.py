import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))


def ex6(n):
    angle = 360 // n
    s = '0 100 180 100 180 0 ' + str(angle) + ' 0 '
    s *= n
    go(s.split())

ex6(int(input()))

input()
