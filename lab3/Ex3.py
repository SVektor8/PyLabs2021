import turtle as trt
from random import randrange, randint

def go(mas):
    for i in range(len(mas) // 2):
        trt.left(mas[2*i])
        trt.forward(mas[2*i + 1])



def f3():
    Vx = 4
    Vy = 11
    Ay = -1
    x, y = 0, 0
    
    for i in range(100):
        x += Vx
        y += Vy + Ay
        Vy += Ay
        
        if round(y) == 0:
            Vy = -Vy
            Vy *= 1
            Vx *= 1
        
        trt.goto(x, y)

f3()

input()
