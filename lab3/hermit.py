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

def fun(x):
    return math.e**(-math.sin(2*x)) + math.sin(2*x) - 1

def dfun(x):
    return 2*(1-math.e**(-math.sin(2*x)))*math.cos(2*x)

def hermie(nodes, x):
    n = len(nodes)
    z = []
    for i in range(n):
        z.append(nodes[i])
        z.append(nodes[i])
    n2 = 2*n
    matrix = np.zeros((n2, n2))
    for i in range(n2):
        for j in range(i+1):
            if j == 0:
                matrix[i][j] = fun(z[i])
            elif j == 1 & i % 2 == 1:
                matrix[i][j] = dfun(z[i])
            else:
                matrix[i][j] = matrix[i][j-1] - matrix[i-1][j-1]
                matrix[i][j] = matrix[i][j] / (z[i] - z[i-j])

    result = 0
    helper = 1
    for i in range(n2):
        result = result + matrix[i][i] * helper
        helper = helper * (x - z[i])
    return result


def chebyshew(x0, x1, n):
    result = []
    for i in range(1, n+1, 1):
        result.append(1/2*(x0 + x1) + 1/2*(x1 - x0)*math.cos((2*i - 1)*math.pi/(2*n)))
    return result


def uniform(x0, x1, n):
    result = []
    for i in range(n):
        result.append(x0 + i*(x1-x0)/(n-1))
    return result

def differenceToSquare(interpolated, values):
    sum = 0
    for i in range(amount):
        sum += (interpolated[i] - values[i])**2
    return sum

def show_plot(points, values, interpolated, x0, x1, n):
    plt.title(f'Interpolation, nodes = {n}')
    # plt.plot(points,values)
    # plt.plot(points, values, 'b-', points, interpolated, 'g-',
    #         chebyshewshew(x0, x1, n), list(map(fun, chebyshewshew(x0, x1, n))), 'r.')
    plt.plot(points, values, 'c-', label='Function')
    plt.plot(points, interpolated, 'r-', label='Interpolating')
    plt.plot(chebyshew(x0, x1, n), functionNodes, 'y.', label='Nodes')

    legend = plt.legend(loc='best', shadow=True, fontsize='small')

    plt.show()



amount = 30000
x0 = 0
x1 = 3*math.pi
points = args(x0, x1, amount)
values = valtab(points)
interpolated = []
# 3 5 6 8 9 10 11 12 15 20


n = 19
for i in range(amount):
    interpolated.append(hermie(chebyshew(x0, x1, n), points[i]))


# diff = []
# for i in range(amount):
#     diff.append(abs(interpolated[i] - values[i]))
#
#
# print(n, max(diff), differenceToSquare(interpolated, values))

functionNodes = []
for i in chebyshew(x0, x1, n):
    functionNodes.append(fun(i))

show_plot(points, values, interpolated, x0, x1, n)
# plt.xlabel('X axis')
# plt.ylabel('Y axis')
# plt.title('Interpolation')
# plt.plot(points, values, 'b-', points, interpolated, 'r-',
#          chebyshew(x0, x1, n), functionNodes, 'y.')
# plt.show()

