import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))

def ex5():
    for i in range(10):
        a = 50 - 5 * i
        go([0, a, 90, a, 90, a, 90, a])

        trt.penup()
        go([180, 2.5, -90, 2.5])
        
        trt.pendown()

ex5()

input()
