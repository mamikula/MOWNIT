
import numpy as np
import random

def jacobi_method(A: np.ndarray, B: np.ndarray, X: np.ndarray, mode: int, eps: float):
    # matrix A must be diagonal dominant
    D = np.diag(A)
    R = A - np.diagflat(D)
    iter_num = 0
    while True:
        X_new = (B - (R @ X)) / D
        iter_num += 1
        if mode == 1:
            if np.linalg.norm(X_new - X) < eps: #norma Frobeniusa jest to pierwiastek z sumy kwadratow wszystkich elementów macierzy
                return X_new, iter_num
        else:
            if np.linalg.norm(A @ X_new - B) < eps:
                return X_new, iter_num
        X = X_new

def get_spectral_radius(A: np.ndarray):
    D = np.diag(A)
    R = A - np.diagflat(D)
    S = R / D
    eigvals = np.linalg.eigvals(S)
    return max(abs(i) for i in eigvals)