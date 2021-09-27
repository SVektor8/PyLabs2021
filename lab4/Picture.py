import turtle as trt
from random import randrange, randint

def go(mas):
    for i in range(len(mas) // 2):
        trt.left(mas[2*i])
        trt.forward(mas[2*i + 1])

def f1():
    for i in range(200):
        go([randrange(360), randrange(200)])

f1()

input()
