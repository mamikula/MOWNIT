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


def fun(x):
    return math.e**(-math.sin(2*x)) + math.sin(2*x) - 1


def lagrange(x, n, nodes):
    #yi wsp przy tych f(xk)
    values = valtab(nodes)

    #Lk
    sum = 0
    for k in range(n):
        term = 1
        for i in range(n):
            if i != k:
                term = term * (x - nodes[i]) / (nodes[k] - nodes[i])
        term = term*values[k]
        sum += term
    return sum


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
interpolated = []

#x dla których wyznaczaa sie wartosc funkcji interpolujacej P(x)
points = args(x0, x1, amount)

#liczba węzłów
n = 38

for i in range(amount):
    interpolated.append(lagrange(points[i], n, chebyshew(x0, x1, n)))

values = valtab(points)
diff = []
for i in range(amount):
    diff.append(abs(interpolated[i] - values[i]))


tmp = [3, 5, 6, 8, 9, 10, 11, 12, 15, 20]

print(n, max(diff), differenceToSquare(interpolated, values))


# 3 5 6 8 9 10 11 12 15 20

functionNodes = []

for i in chebyshew(x0, x1, n):
    functionNodes.append(fun(i))

plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Interpolation')


plt.plot(points, values, 'c-', points, interpolated, 'm-',
         chebyshew(x0, x1, n), functionNodes, 'y.')

# plt.plot(points, values, 'b-',  functionNodes, 'y.')
plt.show()





# 40 0.002311252617665016 0.01598391639446983
# 40 0.007042230178647075 0.02008436674164186

# 42 0.0013241145247832042 0.005609437083718094
# 42 0.025898534412521188 0.07933987980271133

# 45 0.0007598819953736902 0.002157511479793198
# 45 0.3493797447951742 14.600371958135005