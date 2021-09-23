import turtle as t

def d(r):
    for i in range(90):
        t.forward(r)
        t.left(2)

def o(r):
    for i in range(180):
        t.forward(r)
        t.left(2)


t.left(90)
t.fillcolor('yellow')
t.begin_fill()
o(8)
t.end_fill()

t.penup()
t.goto(-300, 65)
t.pendown()

t.fillcolor('blue')
t.begin_fill()
o(1)
t.end_fill()

t.penup()
t.goto(-100, 65)
t.pendown()

t.fillcolor('blue')
t.begin_fill()
o(1)
t.end_fill()

t.penup()
t.goto(-225, 35)
t.pendown()

t.width(10)
t.goto(-225, -20)
t.end_fill()

t.penup()
t.goto(-300, -35)
t.pendown()

t.right(180)
t.width(15)
t.color('red')
d(3)
