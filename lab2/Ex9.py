import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))



def ex9h(n, a):
    angle = 180 - 180 * (n - 2) // n
    s = '0 ' + str(a) + ' '  + str(angle) + ' 0 '
    s *= n
    go(s.split())

def ex9():
    for i in range(3, 13):
        ex9h(i, i*10)
        trt.penup()
        go([-90, 5, -90, 5, 180, 0])
        trt.pendown()

ex9()

input()
