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



def ex10():
    for i in range(6):
       ex4(200)
       trt.left(60) 

ex10()

input()
