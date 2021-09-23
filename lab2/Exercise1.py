import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))

def ex2():
    go([0, 50, 90, 50, 90, 50, 90, 50, 90, 50])

ex2()

input()
