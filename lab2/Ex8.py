import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))



def ex8():
    s = ''
    for i in range(10 * 4):
        a = 5 + 5 * i 
        s += '0 ' + str(a) + ' 90 0 '
    go(s.split())

ex8()

input()
