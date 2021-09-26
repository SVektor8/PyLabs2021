import turtle as trt
from random import randrange, randint

def go(mas):
    for i in range(len(mas) // 2):
        trt.left(mas[2*i])
        trt.forward(mas[2*i + 1])

trt.penup()
trt.goto(-200, 200)
trt.pendown()
go([0, 400, -90, 400, -90, 400, -90, 400])


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
