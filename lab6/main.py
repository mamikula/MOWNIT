import math
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from math import sin, cos
from math import pi

def abs_diff(F, f, xs):
    return [abs(F(x) - f(x)) for x in xs]

def max_diff(F, f, xs):
    return max(abs_diff(F, f, xs))

def sum_sq_diff(F, f, xs):
    return sum(d ** 2 for d in abs_diff(F, f, xs))

def calc_error(F, f, a, b, N=1000):
    xs = np.linspace(a, b, N)
    diffs = abs_diff(F, f, xs)
    return {
        'max': max(diffs),
        'sq': sum(x ** 2 for x in diffs)
    }

def show_error(F, fs, a, b, N, *, prec=4):
    for f, label in fs:
        err = calc_error(F, f, a, b, N)
        print(
                'Największa bezwzględna różnica ', err['max'],
                '       Suma kwadratów różnic ', err['sq'],
        )

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
    else:
        ax.title.set_text(title)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
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
    def __init__(self, approx_method, color='b', label='', args=(), kwargs={}):
        self.im = approx_method
        self.color = color
        self.label = label
        self.args = args
        self.kwargs = kwargs


def rich_plot(fn_obj,
              im_objs: list[PlotApprox],
              a, b, n, *,
              step=.01, N=1000,
              nodes_calc_method=np.linspace,
              nodes_color='#000',
              error_prec=4):
    xs = nodes_calc_method(a, b, n)
    ys = np.vectorize(fn_obj.f)(xs)
    W_objs = [PlotFn(obj.im(xs, ys, *obj.args, **obj.kwargs), obj.color, obj.label) for obj in im_objs]
    fig, ax = plt.subplots(1, 1, figsize=(9, 7))
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fns = [fn_obj] + W_objs
    plot_fns(fns, a, b, step=step, ax=ax)
    ax.scatter(xs, ys, c=nodes_color)
    ax.grid(visible=True)
    xs_ = np.linspace(a, b, N)
    for i, W_obj in enumerate(W_objs):
        diffs = abs_diff(fn_obj.f, W_obj.f, xs_)
    plt.show()
    show_error(fn_obj.f, [(W.f, W.label) for W in W_objs], a, b, N, prec=error_prec)



f = lambda x: (math.e**(-sin(2*x)) + sin(2*x) - 1)

a = 0
b = 3 * pi
x = [a, b]

def g(x):
    return f(x)

# plt.figure(figsize=(15, 5))
# plot_fn(g, a, b, step=.01, color='#0070c0')

def trigonometric_approximation(xs, ys, m):
    n = len(xs)
    a = xs[0]
    b = xs[-1]
    a_trans = -pi
    b_trans = pi

    def transform_x(x):
        return ((x - a) / (b - a)) * (b_trans - a_trans) + a_trans

    def calc_ak(k: int) -> float:
        return 2 / n * sum(ys[i] * cos(k * xs[i]) for i in range(n))

    def calc_bk(k: int) -> float:
        return 2 / n * sum(ys[i] * sin(k * xs[i]) for i in range(n))

    xs = list(map(transform_x, xs))
    ak = list(map(calc_ak, range(m + 1)))
    bk = list(map(calc_bk, range(m + 1)))

    def f(x):
        x = transform_x(x)
        return .5 * ak[0] + sum(ak[k] * cos(k * x) + bk[k] * sin(k * x) for k in range(1, m))

    return f

def plot(n, m):
    print("Liczba węzłów: ", n, "Stopień wielomianu: ", m)
    rich_plot(
        PlotFn(g, "b", "Wyjściowa funkcja"),
        [
            PlotApprox(trigonometric_approximation, 'm', 'Aproksymacja średniokwadratowa', args=(m,)),
        ],
        a, b, n,
        nodes_color='r'
    )

# n = 9
# for m in range(2, 5):
#     plot(n, m)
# for n in [9, 11, 15, 18, 22, 100]:
#     for m in [4, 6, 7, 9, 10, 18, 33, 49]:
#         if n // 2 > m:
#             plot(n, m)

# for n in [25, 50, 100]:
#     for m in [6, 7, 8, 12, 24, 49]:
#         if n // 2 > m:
#             plot(n, m)

n = 100
m = 18
plot(n, m)
