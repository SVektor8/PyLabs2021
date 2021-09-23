import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))



def ex12():
     trt.left(90)
     for i in range(5):
          s = ('1 ' * 360)
          s += ('5 1 ' * 36)
          go(s.split())

ex12()

input()
