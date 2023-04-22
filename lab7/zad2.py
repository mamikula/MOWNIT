import numpy as np
import pandas as pd
pd.options.display.float_format = "{:,.12f}".format

def newton_matrix(F, J, X, epsilon, exit):
    X = np.array(X)
    iters = 0
    while True:
        A = np.copy(X)
        try:
            S = np.linalg.solve(J(X), F(X))
        except np.linalg.LinAlgError:
            return [' - ', ' - ', ' - '], ' - '
        X = X - S
        iters += 1
        if exit == 1:
            if np.linalg.norm(X-A) < epsilon: return X, iters
        elif exit == 2:
            if np.linalg.norm(F(X)) < epsilon: return X, iters
        if iters > 500:
            return [' - ', ' - ', ' - '], ' - '


def F(X):
    ret = [0,0,0]
    ret[0] = X[0]**2 + X[1]**2 + X[2] - 1
    ret[1] = 2*X[0]**2 + X[1]**2 + X[2]**3 - 2
    ret[2] = 3*X[0] - 2*X[1]**3 - 2*X[2]**2 - 3
    return ret

def J(X):
    ret = [[2*X[0],   2*X[1],       1],
           [4*X[0],   2*X[1],       3*X[2]**2 ],
           [3,       -6*X[1]**2,    -4*X[2]]]
    return ret


for end1 in [-1, -0.6, -0.2, 0.2, 0.6, 1]:
    for end2 in [-1, -0.6, -0.2, 0.2, 0.6, 1]:
        for end3 in [-1, -0.6, -0.2, 0.2, 0.6, 1]:
            print(f"[{end1:.1f}, {end2:.1f}, {end3:.1f}]", end="  ")
            for prec in [0.001, 0.0001, 0.00001, 0.000001]:
                x1, iters1 = newton_matrix(F, J, [end1, end2, end3], prec, 1)
                x2, iters2 = newton_matrix(F, J, [end1, end2, end3], prec, 2)
                if prec != 0.000001:
                    print(f"{x1}", end=" | ")
                else:
                    print(f"{x1}")

