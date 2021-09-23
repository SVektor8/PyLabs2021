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


def ex11():
    trt.left(90)
    for i in range(10):
        ex4(57 + 58*i)
    trt.left(180)
    for i in range(10):
        ex4(57 + 58 * i)

ex11()

input()
