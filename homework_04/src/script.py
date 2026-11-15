import time
import numpy as np

# ── Данные: 200 000 строк по 5 чисел ───────────────────────
rng = np.random.default_rng(42)
m = rng.normal(size=(200_000, 5))


# ── Способ 1: циклы ────────────────────────────────────────
def loop_version(mat:np.ndarray):
    n, k = mat.shape

    # сумма каждой строки
    row_sums = [0.0] * n
    for i in range(n):
        for j in range(k):
            row_sums[i] += mat[i, j]

    # максимум и его индекс по каждому столбцу
    col_max = [0.0] * k
    col_arg = [0] * k
    for j in range(k):
        col_max[j] = mat[0, j]
        for i in range(1, n):
            if mat[i, j] > col_max[j]:
                col_max[j] = mat[i, j]
                col_arg[j] = i
    return row_sums, col_max, col_arg


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy_version(mat:np.ndarray):
    return mat.sum(axis=1), mat.max(axis=0), mat.argmax(axis=0)


# ── Замер: 3 раза, берём лучший ────────────────────────────
def measure(fn, x, repeat=3):
    best = float("inf")
    result = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        result = fn(x)
        t1 = time.perf_counter()
        best = min(best, t1 - t0)
    return result, best


(r_loop,  t_loop)  = measure(loop_version,  m)
(r_numpy, t_numpy) = measure(numpy_version, m)

print(f"цикл:   {t_loop*1000:10.2f} мс")
print(f"NumPy:  {t_numpy*1000:10.2f} мс")
print(f"ускорение: {t_loop / t_numpy:.1f}×")
print()
print("суммы строк совпадают:  ", np.allclose(r_loop[0], r_numpy[0]))
print("максимумы совпадают:    ", np.allclose(r_loop[1], r_numpy[1]))
print("индексы совпадают:      ", np.array_equal(r_loop[2], r_numpy[2]))
print()
print("NumPy, максимумы по столбцам:", np.round(r_numpy[1], 4))
print("NumPy, их индексы:           ", r_numpy[2])
