from header import jacobi_method, get_spectral_radius
import numpy as np
import time
import random
k = 5
m = 4

for n in range(3,101, 4):
    print(f"{n}", end=" & ")
    for index, prec in enumerate([1e-2, 1e-4, 1e-5, 1e-6, 1e-10]):
        A = np.array([[k if i == j else 1/(abs(i-j)+m) for i in range(1,n+1)] for j in range(1,n+1)])
        X_known = np.array([1 if i%2==0 else -1 for i in range(n)])


        B = A @ X_known
        # X_start = np.array([0 for _ in range(n)])
        X_start = np.array([random.randint(-10e10, 10e10) for _ in range(n)])
        start = time.time()
        # for k in range(1000):
        X, iters = jacobi_method(A, B, X_start, 1, prec)
        stop = time.time()
        calc_time = stop-start
        norm = np.linalg.norm(X_known-X)

        if prec != 10e-10:
            # print(f"{norm:.4e}", end=" & ")  # error
            # print(f"{calc_time/1000:.7f}", end=" & ")  # time
            print(f"{iters}", end=" & ")  # iterations
        else:
            # print(f"{norm:.4e}", end="\n")  # error
            # print(f"{calc_time/1000:.7f}", end="\n")  # time
            print(f"{iters}", end="\n")  # iterations

# for n in range(3,128, 4):
#     print(f"{n}", end=" & ")
#     A = np.array([[k if i == j else 1/(abs(i-j)+m) for i in range(1,n+1)] for j in range(1,n+1)])
#     print(f"{get_spectral_radius(A):.5f}")