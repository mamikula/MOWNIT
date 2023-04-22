from header import gaussian_elimination, thomas_alg
import numpy as np
import time

k = 6
m = 4


for n in range(20, 1003, 20):
# for n in range(100, 501, 50):
# for n in [3, 4, 6, 8, 10, 12, 14 ,16, 18]:

    print(n, end=" & ")
    # for fltype in (np.float32, np.float64, np.float128):
    A = np.zeros((n, n)).astype(np.float64)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                A[i - 1, j - 1] = k
            elif j == i + 1:
                A[i - 1, j - 1] = 1 / (i + m)
            elif i > j and j == i - 1:
                A[i - 1, j - 1] = k / (i + m + 1)

    X_known = np.array([1 if i % 2 == 0 else -1 for i in range(n)]).astype(np.float64)
    B = A @ X_known
    gauss_start = time.time()
    X_g = gaussian_elimination(A, B)
    gauss_end = time.time()
    thomas_start = time.time()
    X_t = thomas_alg(A, B)
    thomas_end = time.time()
    # norm_g = np.linalg.norm(X_known - X_g)
    # norm_t = np.linalg.norm(X_known - X_t)
    print(f"{gauss_end-gauss_start:.50f} & {thomas_end-thomas_start:.50f}", end="\n")
    # print(f"{norm_g:.5e} & {norm_t:.5e} ")
    # print("[", end="")
    # for i in X_g:
    #     print(f"{i: .8}", ", ", end="")
    #     # print(i, ", ", end="")
    # print("]", end="")
    # print(end=" & ")
    # print("[", end="")
    # for i in X_t:
    #     print(f"{i: .8}", ", ", end="")
    #     # print(i, ", ", end="")
    # print("]", end="")
    # print(end="\n")