import math
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

def abs_diff(f, W, xs): #norma z różnicy
    return [abs(f(x) - W(x)) for x in xs]

def max_diff(f, W, xs): #największa różnica
    return max(abs_diff(f, W, xs))


def show_error(f, Ws, a, b, N, *, prec=6): #funkcja do wyliczania błędów
    xs = np.linspace(a, b, N)

    for W, label in Ws:
        diffs = abs_diff(f, W, xs)
        print(max(diffs), sum(x ** 2 for x in diffs))

def plot_fn(fn, a, b, *, label='', title='Wykres', color='b', step=.1, ax=plt):
    n = int((b - a) / step) + 1
    xs = np.linspace(a, b, n)
    ys = np.vectorize(fn)(xs)
    ax.plot(xs, ys, color, label=label)
    if label: ax.legend(loc='best')

    if ax is plt:
        ax.title(title)
        ax.xlabel('x')
        ax.ylabel('y')
    ax.grid()

    sns.despine()

class PlotFn:
    def __init__(self, f, color='b', label=''):
        self.f = f
        self.color = color
        self.label = label

def plot_fns(fns: list[PlotFn], a, b, *, title='Wykres', step=.1, ax=plt):
    for fn_obj in fns:
        plot_fn(fn_obj.f, a, b, title=title, step=step, ax=ax, color=fn_obj.color, label=fn_obj.label)


class PlotApprox:
    def __init__(self, approx_method, color='m', label='', args=(), kwargs={}):
        self.im = approx_method
        self.color = color
        self.label = label
        self.args = args
        self.kwargs = kwargs


def rich_plot(fn_obj: 'Funkcja wyjściowa',
              im_objs: list[PlotApprox],
              a, b, n, *,
              step=.01,
              N=1000,
              nodes_calc_method=np.linspace,
              error_prec=6):
    xs = nodes_calc_method(a, b, n)
    ys = np.vectorize(fn_obj.f)(xs)
    W_objs = [PlotFn(obj.im(xs, ys, obj.args, **obj.kwargs), obj.color, obj.label) for obj in im_objs]

    fig, ax = plt.subplots(1, 1, figsize=(9, 7))

    # Compare approximation to the original function
    fns = [fn_obj] + W_objs
    plot_fns(fns, a, b, step=step, ax=ax)
    ax.scatter(xs, ys)
    ax.grid(visible=True)

    xs_ = np.linspace(a, b, N)
    for i, W_obj in enumerate(W_objs):
        diffs = abs_diff(fn_obj.f, W_obj.f, xs_)

    plt.show()

    show_error(fn_obj.f, [(W.f, W.label) for W in W_objs], a, b, N, prec=error_prec)



f = lambda x: (math.e**(-math.sin(2*x)) + math.sin(2*x) - 1)

a = 0
b = 3 * math.pi
x = [a, b]

def g(x):
    return f(x)

plt.figure(figsize=(12, 8))
plot_fn(g, a, b, step=.01)



def mean_square_approximation(xs, ys, m: 'degree of a plynomial'):

    n = len(xs)
    G = np.zeros((m, m), float)
    B = np.zeros(m, float)

    sums = [sum( xs[i] ** k for i in range(n)) for k in range(2 * m + 1)]

    for j in range(m):
        for k in range(m):
            G[j, k] = sums[j + k]

        B[j] = sum(ys[i] * xs[i] ** j for i in range(n))

    A = np.linalg.solve(G, B)
    return lambda x: sum(A[i] * x ** i for i in range(m))

# n = 100
# m = 35

# xs = np.linspace(a, b, n)
# ys = np.vectorize(g)(xs)
# mean_square_approximation(xs, ys, m)

for n in [10, 15, 20, 25, 50, 100, 500]:
    for m in [4, 6, 8, 10]:

        xs = np.linspace(a, b, n)
        ys = np.vectorize(g)(xs)
        mean_square_approximation(xs, ys, m)

        print("Liczba węzłów: " , n,"Stopień wielomianu: ", m)
        rich_plot(
            PlotFn(g, "#777", "Funkcja zadana"),
            [
                PlotApprox(mean_square_approximation, '#7A06C3', 'Funkcja aproksymujaca', m),
            ],
            a, b, n
        )