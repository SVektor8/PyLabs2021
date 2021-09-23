import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))


def ex14(n):
    angle =  (180 - 180 * (n - 2) // n) * 2
    s = str(angle) + ' 150 '
    s *= n
    go(s.split())

ex14(int(input()))

input()
