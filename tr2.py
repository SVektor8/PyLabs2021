import turtle as trt
from random import randrange, randint

def go(mas):
    for i in range(len(mas) // 2):
        trt.left(mas[2*i])
        trt.forward(mas[2*i + 1])

def f1():
    for i in range(200):
        go([randrange(360), randrange(200)])

nums = [[90, 100, -90, 50, -90, 100, -90, 50, 180, 50, 90, 100, -90, 0],
        [45, 71, -135, 100, 180, 100, -90, 0],
        [],
        [],
        [90, 50, 180, 50, 90, 50, 90, 50, 180, 100, 180, 100, -90, 0],
        [],
        [],
        [0, 50, -135, 71, 45, 50, 180, 50, -45, 71, -45, 0],
        [],
        []]

pre = [[0, 20, -90, 100, 90, 0],
       [0, 20, -90, 50, 90, 0],
       [],
       [],
       [0, 20, -90,  50, 90, 0],
       [],
       [],
       [0, 20],
       [],
       []]

def f2():
    ind = [1,4, 1, 7, 0, 0]
    for i in ind:
        trt.penup()
        go(pre[i])
        trt.pendown()
        go(nums[i])

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

def f4():
    num = 10
    steps = 10000
    
    pool = [[trt.Turtle(shape = 'turtle'), 0, 0, 0, 0] for  i in range(num)]
    for unit in pool:
        unit[0].penup()
        unit[0].speed(50)
        unit[1], unit[2] = randint(-200, 200), randint(-200, 200)
        unit[3], unit[4] = randint(-5, 5), randint(-5, 5)
        unit[0].goto(unit[1], unit[2])

    for i in range(steps):
        for unit in pool:
            unit[1] += unit[3]
            unit[2] += unit[4]
            if abs(unit[1]) >= 201:
                unit[3] = - unit[3]
            if abs(unit[2]) >= 201:
                unit[4] = - unit[4]
            unit[0].goto(unit[1], unit[2])

f4()

input()
