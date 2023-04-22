import numpy as np
import pandas as pd

def norm(A):
    n = len(A)
    return max(sum(A[i][j] for j in range(n)) for i in range(n))

def create_A1(n):
    return np.array([[1 / (i + j - 1) if i != 1 else 1 for j in range(1, n + 1)] for i in range(1, n + 1)])

def create_A2(n):
    A = np.zeros((n, n))
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if j >= i:
                A[i - 1][j - 1] = 2 * i / j
            else:
                A[i - 1][j - 1] = A[j - 1][i - 1]
    return A

def conditioning_factor(A):
    A_inv = np.linalg.inv(A)
    return norm(A_inv) * norm(A)


def condition_number(numbers):
    result = []
    for n in numbers:
        con_num_1 = conditioning_factor(create_A1(n))
        con_num_2 = conditioning_factor(create_A2(n))
        result += [con_num_1, con_num_2]
    df = pd.DataFrame(data={"n":numbers,
                            "ex 1 condition number":result[::2],
                            "ex 2 condition number":result[1::2]})
    print(df)
    return df

numbers = [3, 4, 6, 8, 10, 12, 14, 16, 18, 20, 20, 30, 50, 70, 100, 150, 200, 300, 500]
condition_df = condition_number(numbers)
condition_df