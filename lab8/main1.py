from header import gaussian_elimination
import numpy as np

for n in range(2, 101, 2):
# for n in [3, 4, 6, 8, 10, 12, 14 ,16, 18]:
    print(n, end=" & ")
    for fltype in (np.float32, np.float64):
        A = np.array([[1/(i+j-1) if i != 1 else 1 for j in range(1,n+1)] for i in range(1,n+1)]).astype(fltype)
        X_known = np.array([1 if i%2==0 else -1 for i in range(n)]).astype(fltype)
        B = A @ X_known
        X = gaussian_elimination(A, B)
        norm = np.linalg.norm(X_known-X)
        if fltype != np.float64:
            print(f"{norm:.5e}", end=" & ")
        else:
            print(f"{norm:.5e}", end="\n")
        # if fltype == np.float64:
        #     for i in X:
        #         print(f"{i: .8}", ", ", end="")
        #         # print(i, ", ", end="")
        #     print(end="\n")
            # print(f"{X}", end=" \n ")
        # else:
        #     print(f"{X}", end="\n")
