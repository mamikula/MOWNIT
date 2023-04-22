import math
# [3/4pi, 3pi]
# k = 0.5
# m = 2
# h duże wziąć


# function to be solved
import numpy as np
from matplotlib import pyplot as plt

k = .5
m = 2

def differenceToSquare(interpolated, values, step):
    sum = 0
    for i in range(step):
        sum += (interpolated[i] - values[i])**2
    return sum

def base_f(x):
    return math.e**(-k*math.cos(m*x))-k*math.cos(m*x)+1

def f(x, y):
    return k*m*y*math.sin(m*x) + k**2*m*math.sin(m*x)*math.cos(m*x)

def rk4(x0, y0, xn, n):
    h = (xn - x0) / n
    y = np.zeros(n)
    y[0] = y0
    for i in range(n - 1):
        k1 = h * (f(x0, y0))
        k2 = h * (f((x0 + h / 2), (y0 + k1 / 2)))
        k3 = h * (f((x0 + h / 2), (y0 + k2 / 2)))
        k4 = h * (f((x0 + h), (y0 + k3)))
        k = (k1 + 2 * k2 + 2 * k3 + k4) / 6
        yn = y0 + k
        y[i + 1] = yn
        y0 = yn
        x0 = x0 + h
    return y

def rk2(x0, y0, xn, n):
    h = (xn - x0) / n
    y = np.zeros(n)
    y[0] = y0
    for i in range(n-1):
        k1 = h * (f(x0, y0))
        k2 = h * (f((x0 + h / 2), (y0 + k1 / 2)))
        k = (k1 + k2) / 2
        yn = y0 + k
        y[i+1] = yn
        y0 = yn
        x0 = x0 + h
    return y

def euler(x0, y0, xn, n):
    h = (xn - x0) / n
    y = np.zeros(n)
    y[0] = y0
    for i in range(n-1):
        y[i+1] = y[i] + f(x0, y[i])*h
        x0 += h
    return y

x0 = math.pi/4
y0 = base_f(x0)
xn = 3*math.pi

steps = [100]
step = 1000

def printSolution():
    for step in steps:
        eulerRes = euler(x0, y0, xn, step)
        rk2res = rk2(x0, y0, xn, step)
        rk4res = rk4(x0, y0, xn, step)

        a = [0] * step
        aFun = [0]*200
        points = np.linspace(x0, xn, step, endpoint=True)
        pointsFun = np.linspace(x0, xn, 200, endpoint=True)
        for i in range(len(points)):
            a[i] = base_f(points[i])

        for i in range(200):
            aFun[i] = base_f(pointsFun[i])

        print(step, '&',f"{differenceToSquare(a, eulerRes, step):.5f}", end=" & ")
        print(f"{differenceToSquare(a, rk2res, step):.5f}", end=" & ")
        print(f"{differenceToSquare(a, rk4res, step):.5f}", end="\n")

        # f"{norm:.4e}"
        plt.title(f'nodes = {step}')
        plt.plot(pointsFun, aFun, 'b')
        plt.plot(points, eulerRes, 'g')
        # plt.plot(points, rk2res, 'g')
        # plt.plot(points, rk4res, 'g')
        # plt.plot(points, a, 'r.', label='Nodes')
        plt.legend(["function","euler"], loc=1)
        plt.show()

printSolution()
# rk4res = rk4(x0, y0, xn, step)
# rk2res = rk2(x0, y0, xn, step)
#
# eulerRes = euler(x0, y0, xn, step)
# a = [0]*step
# points = np.linspace(x0, xn, step, endpoint=True)
# for i in range(len(points)):
#     a[i] = base_f(points[i])
#
# print(differenceToSquare(a, eulerRes))
#
# plt.plot(points, a, 'b')
# plt.plot(points, eulerRes, 'g')
# # plt.plot(points, rk4res, 'g')
# # plt.plot(points, eulerRes, 'g')
# # plt.plot(points, a, 'r.', label='Nodes')
# plt.legend(["function", "RK2"], loc=1)
# plt.show()

