import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))

def ex4(radius):
    s = ('1 ' + str(round(radius * 2 * 3.1415926 / 360)) + ' ') * 360
    go(s.split())

ex4(200)

input()
