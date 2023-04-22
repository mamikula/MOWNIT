import math

import pandas as pd

a = .2
b = 2
f = lambda x : 40*x*math.e**(-8) - 40*math.e**(-8*x) + 1/40


stop_criterion_init1 = lambda ro: lambda _, x_prev, x_curr: abs(x_curr - x_prev) < ro
stop_criterion_init2 = lambda ro: lambda f, _, x_curr: abs(f(x_curr)) < ro

fi_init = lambda f, deriv_f: lambda x: x - f(x) / deriv_f(x)
f_deriv = lambda x: 320*math.e**(-8*x) + 40/math.e**8


def newton_raphson(f, f_deriv, x0, stop_criterion):
    x_prev = float('inf')
    x_curr = x0
    fi = fi_init(f, f_deriv)
    iters = 0

    while not stop_criterion(f, x_prev, x_curr):
        x_curr, x_prev = fi(x_curr), x_curr
        iters += 1

    return x_curr, iters


def calculate(a, b, stop_criterion_init, ro_list, step=.1):
    n = int(abs(b - a) / step + .5)
    x0_list = [a + step * i for i in range(n)] + [b]
    stop_criterions = list(map(stop_criterion_init, ro_list))

    df = pd.DataFrame(columns=ro_list, index=x0_list)

    for i, x0 in enumerate(x0_list):
        for j, ro in enumerate(ro_list):
            df.iloc[i, j] = newton_raphson(f, f_deriv, x0, stop_criterions[j])

    return df

# df1 = calculate(a, b, stop_criterion_init1, [
#     1e-15
# ])


# print(df1)
# df2 = calculate(a, b, stop_criterion_init2, [
#     1e-15
# ])



def calc_xi2(f, xi0, xi1):
    return xi1 - (xi1 - xi0) / (f(xi1) - f(xi0)) * f(xi1)


def secant_method(f, x0, x1, stop_criterion):
    xi0 = None
    xi1 = x0
    xi2 = x1
    iters = 0

    while not stop_criterion(f, xi1, xi2):
        xi2, xi1, xi0 = calc_xi2(f, xi2, xi1), xi2, xi1
        iters += 1

    return xi2, iters


def calculate(a, b, x1, stop_criterion_init, ro_list, step=.1):
    if not a <= x1 <= b:
        raise Exception(f'x1={x1} is not between {a} and {b}')

    if x1 - a < b - x1:
        a = x1
    else:
        b = x1

    n = int(abs(b - a) / step + .5)
    if a == x1:
        x0_list = [a + step * i for i in range(1, n)] + [b]
    else:
        x0_list = [a + step * i for i in range(n)]

    stop_criterions = list(map(stop_criterion_init, ro_list))
    dec_places = len(str(int(1 / step + .5)))

    df = pd.DataFrame(columns=ro_list, index=[(round(min(x0, x1), dec_places), round(max(x0, x1), dec_places)) for x0 in x0_list])

    for i, x0 in enumerate(x0_list):
        for j, ro in enumerate(ro_list):
            df.iloc[i, j] = secant_method(f, x0, x1, stop_criterions[j])

    return df

# df1 = calculate(a, b, a, stop_criterion_init1, [
#     1e-15
# ])
# print(df1)
#
df2 = calculate(a, b, a, stop_criterion_init2, [
    1e-10
])

# print(secant_method(f, .3, 1.6, stop_criterion_init2(1e-3)))
print(df2)