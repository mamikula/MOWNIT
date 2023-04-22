import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
import math



def save(filename, results):
    filename += '.xlsx'
    df = DataFrame(data=results)
    print(df)


def f(x):
    return math.e**(-math.sin(2*x)) + math.sin(2*x) - 1


def spline3(x_points, y_points, xs, boundary_cond):
    size = len(x_points) - 2
    matrix = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i][j] = 4
            if j == i+1 or j == i-1:
                matrix[i][j] = 1

    if boundary_cond == 2:
        matrix[0][0] = 5
        matrix[size - 1][size - 1] = 5

    g = np.zeros(size)
    h = x_points[1] - x_points[0]
    for i in range(size):
        g[i] = 6 / (h**2) * (y_points[i] - 2*y_points[i+1] + y_points[i+2])
    z = np.linalg.solve(matrix, g)

    z = list(z)
    if boundary_cond == 1:
        #cubic spline
        # dołączam do tablicy rozwiązań warunek brzegowy
        z = [0] + z + [0]
    else:
        # Parabolic Spline
        # dołączam do tablicy rozwiązań warunek brzegowy
        z = [z[0]] + z + [z[-1]]

    a = []; b = []; c = []; d = []
    for i in range(size+1):
        a.append((z[i+1] - z[i]) / (6 * h))
        b.append(0.5 * z[i])
        c.append((y_points[i+1] - y_points[i]) / h - (z[i+1] + 2 * z[i]) / 6 * h)
        d.append(y_points[i])

    nr_fun = 0
    ys = []
    for i in range(len(xs)):
        while x_points[nr_fun + 1] < xs[i] < x_points[-1]:
            nr_fun += 1
        ys.append(get_val([d[nr_fun], c[nr_fun], b[nr_fun], a[nr_fun]], x_points[nr_fun], xs[i]))

    return ys


def spline2(x_points, y_points, xs, boundary_cond):
    size = len(x_points) - 1
    matrix = np.zeros((size, size))

    for i in range(size):

        for j in range(size):
            if i == j:
                matrix[i][j] = 1
            if j == i-1:
                matrix[i][j] = 1

    g = np.zeros(size)
    h = x_points[1] - x_points[0]
    for i in range(size):
        g[i] = 2 / h * (y_points[i+1] - y_points[i])
    b = np.linalg.solve(matrix, g)

    # the boundary condition is set here
    b = list(b)
    if boundary_cond == 1:
        # natural cubic spline
        b = [0] + b
    elif boundary_cond == 2:
        # clamped boundary(pierwsze pochodne przybliżone ilorazami różnicowymi)
        b = [(y_points[1] - y_points[0]) / (x_points[1] - x_points[0])] + b


    a = []; c = []
    for i in range(size):
        a.append((b[i+1] - b[i]) / (2 * h))
        c.append(y_points[i])
    if boundary_cond == 2:
        a[0] = 0

    nr_fun = 0
    ys = []
    for i in range(len(xs)):

        while x_points[nr_fun + 1] < xs[i] < x_points[-1]:
            nr_fun += 1
        ys.append(get_val([c[nr_fun], b[nr_fun], a[nr_fun]], x_points[nr_fun], xs[i]))
    return ys



def get_norm(interpolated, values, which):
    valtab = []
    for i in range(n_draw):
        valtab.append(f(i))

    if which == "normax":
        diff = []
        for i in range(n_draw):
            diff.append(abs(interpolated[i] - values[i]))
        return max(diff)
    if which == "sqdif":
        sum = 0
        for i in range(n_draw):
            sum += (interpolated[i] - values[i]) ** 2
        return sum


def get_xs(a, b, n): #rozkład równomierny
    step = (b-a)/(n-1)
    ret = []
    for i in range(n):
        ret.append(a)
        a += step
    return ret


def get_ys(xs):
    return [f(x) for x in xs]


def get_val(coeff, xi, x):
    val = 0
    for i, elem in enumerate(coeff):
        val += elem * (x - xi) ** i
    return val


start = 0
end = 3*math.pi
n_points = 8
n_draw = 1000
spline = 2


xs = get_xs(start, end, n_draw) #rozkład równomierny X
ys_or = get_ys(xs) #rozkład równomierny Y
res = [['Liczba węzłów', 'spl2, nat', 'spl2, lin', 'spl3, nat', 'spl3, par']]



# nodes = [13, 17, 27]
nodes = [5, 8, 10, 15, 20, 25, 30, 35, 50, 75, 100]
# nodes = [ 300, 400, 500, 700]
for i in nodes:
# for i in range(7, 27):
    print(i)
    plt.figure(figsize=(12, 6))
    xp = get_xs(start, end, i) #rozkład równomierny X węzłów
    yp = get_ys(xp) #rozkład równomierny Y węzłów

    #wykres funkcji
    # plt.plot(xp, yp, 'r.', markersize=14)
    plt.plot(xs, ys_or, 'b', label='Interpolated')
    plt.plot(xp, yp, 'r.', markersize=10)
    r = [i]

    #if True: #spline == 2 or spline == 0:
    ys = spline2(xp, yp, xs, 1) #wartości funcji w punktach dla danej liczby węzłów ys
    plt.plot(xs, ys, 'g', label='2nd degree natural cubic spline:')
    r.append(get_norm(ys, ys_or, 'normax'))
    ys = spline2(xp, yp, xs, 2)
    plt.plot(xs, ys, 'm', label='2nd degree clamped boundary spline')
    r.append(get_norm(ys, ys_or, 'normax'))

    #if True: #spline == 3 or spline == 0:
    ys = spline3(xp, yp, xs, 1)
    plt.plot(xs, ys, 'grey', label='3rd degree natural cubic spline')
    r.append(get_norm(ys, ys_or, 'normax'))
    ys = spline3(xp, yp, xs, 2)
    plt.plot(xs, ys, 'y', label='3rd degree parabolic runout spline')
    r.append(get_norm(ys, ys_or, 'normax'))
    res.append(r)

    s = "plot" + str(i) + ".pdf"
    plt.title(f'nodes: {i}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(fontsize = 'small')
    # plt.savefig(s)
    plt.show()

save('res_eq', res)

