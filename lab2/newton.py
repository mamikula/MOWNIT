import numpy as np
import math
import matplotlib.pyplot as plt


def valtab(nodes):
    values = []
    for node in nodes:
        values.append(fun(node))

    return values

#x dla których wyznaczaa sie wartosc funkcji interpolujacej P(x)
def args(x0, x1, amount):
    tab = []
    for x in range(0, amount):
        tab.append(x0 + x*(x1-x0)/amount)
    return tab

#węzły dla których obliczana jest wartość P(x)
def uniform(x0, x1, n):#nodes
    result = []
    for i in range(n):
        result.append(x0 + i*(x1-x0)/(n-1))

    return result


def countTable(nodes, values):
    n = len(nodes)
    a = []
    for i in range(n):
        a.append(values[i])

    for j in range(1, n):

        for i in range(n-1, j-1, -1):
            a[i] = float(a[i]-a[i-1])/float(nodes[i] - nodes[i - j])

    return np.array(a)


def newton(x, nodes):
    a = countTable(nodes, valtab(nodes))

    n = len(a) - 1
    temp = a[n]
    for i in range(n - 1, -1, -1):
        temp = temp * (x - nodes[i]) + a[i]
    return temp


def fun(x):
    return math.e**(-math.sin(2*x)) + math.sin(2*x) - 1


def chebyshew(x0, x1, n):
    result = []
    for i in range(1, n+1, 1):
        result.append(1/2*(x0 + x1) + 1/2*(x1 - x0)*math.cos((2*i - 1)*math.pi/(2*n)))
    return result

def differenceToSquare(interpolated, values):
    sum = 0
    for i in range(amount):
        sum += (interpolated[i] - values[i])**2
    return sum

amount = 30000
x0 = 0
x1 = 3*math.pi
points = args(x0, x1, amount)

values = valtab(points)

interpolated = []
# 3 5 6 8 9 10 11 12 15 20

n = 45
for i in range(amount):
    interpolated.append(newton(points[i], chebyshew(x0, x1, n)))


diff = []
for i in range(amount):
    diff.append(abs(interpolated[i] - values[i]))

print(n, max(diff), differenceToSquare(interpolated, values))


functionNodes = []
for i in chebyshew(x0, x1, n):
    functionNodes.append(fun(i))


#
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Interpolation')

plt.plot(points, values, 'c-', points, interpolated, 'm-',
         chebyshew(x0, x1, n), functionNodes, 'y.')

plt.show()