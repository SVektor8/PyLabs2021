import turtle as trt
from math import sin, cos

def go(args):
    for i in range(len(args)):
        if i % 2 == 0:
            trt.left(int(args[i]))
        else:
            trt.forward(int(args[i]))

def ex2():
    go([0, 50, 90, 50, 90, 50, -90, 50, -90, 50])

def ex3():
    go([0, 50, 90, 50, 90, 50, 90, 50])

def ex4(radius):
    s = ('1 ' + str(round(radius * 2 * 3.1415926 / 360)) + ' ') * 360
    go(s.split())

def ex5():
    for i in range(10):
        a = 50 - 5 * i
        go([0, a, 90, a, 90, a, 90, a])

        trt.penup()
        go([180, 2.5, -90, 2.5])
        
        trt.pendown()

def ex6(n):
    angle = 360 // n
    s = '0 100 180 100 180 0 ' + str(angle) + ' 0 '
    s *= n
    go(s.split())

def ex7():
    s = ''
    for i in range(720):
        r = 200 / 2 * i / 180 
        trt.goto(round(r * cos(i / 180 * 3.1415926)), round(r * sin(i/180 * 3.1415926)))

def ex8():
    s = ''
    for i in range(10 * 4):
        a = 5 + 5 * i 
        s += '0 ' + str(a) + ' 90 0 '
    go(s.split())

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

def ex10():
    for i in range(6):
       ex4(200)
       trt.left(60) 

def ex11():
    trt.left(90)
    for i in range(10):
        ex4(57 + 58*i)
    trt.left(180)
    for i in range(10):
        ex4(57 + 58 * i)

def ex12():
     trt.left(90)
     for i in range(5):
          s = ('1 ' * 360)
          s += ('5 1 ' * 36)
          go(s.split())
      
def ex14(n):
    angle =  (180 - 180 * (n - 2) // n) * 2
    s = str(angle) + ' 150 '
    s *= n
    go(s.split())

input()
