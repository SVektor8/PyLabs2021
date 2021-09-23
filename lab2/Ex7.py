import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))


def ex7():
    s = ''
    for i in range(720):
        r = 200 / 2 * i / 180 
        trt.goto(round(r * cos(i / 180 * 3.1415926)), round(r * sin(i/180 * 3.1415926)))

ex7()

input()
