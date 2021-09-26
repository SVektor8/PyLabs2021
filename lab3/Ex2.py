import turtle as trt
from random import randrange, randint

def go(mas):
    for i in range(len(mas) // 2):
        trt.left(mas[2*i])
        trt.forward(mas[2*i + 1])

with open('numbers.txt', 'r') as f:
    nums = [[int(j) for j in i.split()] for i in f.read().splitlines()]

def f2():
    ind = [int(i) for i in input("give digits splitted with ' '").split()]
    for i in ind:
        trt.penup()
        go([0, 70])
        trt.pendown()
        go(nums[i])

f2()
input()
