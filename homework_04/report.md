Вспомогательная функция для измерения времени


```python
import math
import time
import numpy as np

def measure(fn, arr, repeat=3):
    best = float("inf")
    result = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        result = fn(arr)
        t1 = time.perf_counter()
        best = min(best, t1 - t0)
    return result, best
```

## Блок 1. Основные операции (задачи 1–4)

**Задача 1. Сумма массива.**
Сравните:
- цикл `for x in a: s += x`;
- `a.sum()`.

Запустите `compare` на $n = 10^5, 10^6, 10^7$ . Постройте таблицу «n → ускорение». Оцените, как ускорение зависит от `n` и почему. В выводе ответьте: при каком `n` разница становится заметной (>10×)?

Постройте таблицу «n → ускорение». Оцените, как ускорение зависит от `n` и почему. В выводе ответьте: при каком `n` разница становится заметной (>10×)?




```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

for n in (100_000, 1_000_000, 10_000_000):
    # данные
    a = rng.normal(size=1_000_000)


    # ── Способ 1: обычный цикл Python ──────────────────────────
    def loop_sum(arr):
        s = 0.0
        for x in arr:
            s += x
        return s


    # ── Способ 2: NumPy ────────────────────────────────────────
    def numpy_sum(arr):
        return arr.sum()

    # ── Сравнение ──────────────────────────────────────────────
    r_loop,  t_loop  = measure(loop_sum,  a)
    r_numpy, t_numpy = measure(numpy_sum, a)

    print(f"Для n = {n:.0e} ==================================")
    print(f"цикл:   {t_loop*1000:10.2f} мс   результат = {r_loop:.6f}")
    print(f"NumPy:  {t_numpy*1000:10.2f} мс   результат = {r_numpy:.6f}")
    print(f"ускорение: {t_loop / t_numpy:.1f}X")
    print(f"результаты совпадают: {np.isclose(r_loop, r_numpy)}")

```

    Для n = 1e+05 ==================================
    цикл:       112.50 мс   результат = 97.502498
    NumPy:        0.48 мс   результат = 97.502498
    ускорение: 233.7X
    результаты совпадают: True
    Для n = 1e+06 ==================================
    цикл:       109.06 мс   результат = 1023.365790
    NumPy:        0.51 мс   результат = 1023.365790
    ускорение: 215.6X
    результаты совпадают: True
    Для n = 1e+07 ==================================
    цикл:       120.74 мс   результат = 885.383718
    NumPy:        0.53 мс   результат = 885.383718
    ускорение: 228.2X
    результаты совпадают: True
    

**Задача 2. Среднее и стандартное отклонение.**
Реализуйте среднее и std:
- «в лоб»: цикл с суммой и суммой квадратов, потом формула;
- NumPy: `a.mean()`, `a.std()`.

Сравните на $n = 10^6$. Проверьте, совпадают ли результаты до $10^-12$ . 




```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

# данные
a = rng.normal(size=1_000_000)


# ── Способ 1: обычный цикл Python ──────────────────────────
def loop_sum(arr):
    mean = 0.0
    for x in arr:
        mean += x
    mean /= len(arr)
    std = 0.0
    for x in arr:
        std += (x - mean)**2
    std = (std / len(arr))**0.5
    return mean, std


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy_sum(arr):
    return arr.mean(), arr.std()

# ── Сравнение ──────────────────────────────────────────────
(mean_loop, std_loop),  t_loop  = measure(loop_sum,  a)
(mean_numpy, std_numpy), t_numpy = measure(numpy_sum, a)

print(f"цикл:   {t_loop*1000:10.2f} мс   результат = {mean_loop:.6f}; {std_loop:.6f}")
print(f"NumPy:  {t_numpy*1000:10.2f} мс   результат = {mean_numpy:.6f}; {std_numpy:.6f}")
print(f"ускорение: {t_loop / t_numpy:.1f}X")
print(f"результаты совпадают: {np.isclose(mean_loop, mean_numpy, rtol=0, atol=1e-12)}; {np.isclose(std_loop, std_numpy, rtol=0, atol=1e-12)}")

```

    цикл:       421.49 мс   результат = 0.000098; 1.000483
    NumPy:        6.39 мс   результат = 0.000098; 1.000483
    ускорение: 66.0X
    результаты совпадают: True; True
    

**Задача 3. Поэлементное преобразование: \(y = \sin(x) + x^2\).**
Реализуйте:
- цикл с `math.sin(x) + x*x`;
- NumPy: `np.sin(a) + a**2`.

Сравните на `n = 10^6`.




```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

# данные
a = rng.normal(size=1_000_000)


# ── Способ 1: обычный цикл Python ──────────────────────────
def loop_sin(arr):
    r = []
    for x in arr:
        r.append(math.sin(x) + x**2)
    return r


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy_sin(arr):
    return np.sin(arr) + arr**2

# ── Сравнение ──────────────────────────────────────────────
r_loop,  t_loop  = measure(loop_sin,  a)
r_numpy, t_numpy = measure(numpy_sin, a)

print(f"цикл:   {t_loop*1000:10.2f} мс")
print(f"NumPy:  {t_numpy*1000:10.2f} мс")
print(f"ускорение: {t_loop / t_numpy:.1f}X")
print(f"результаты совпадают: {all(np.isclose(r_loop, r_numpy))}")

```

    цикл:       380.44 мс
    NumPy:       17.48 мс
    ускорение: 21.8X
    результаты совпадают: True
    

**Задача 4. Условная замена (clipping).**
Замените все значения `< 0` на 0, все `> 1` на 1:
- «в лоб»: цикл с `if/elif`;
- NumPy: `np.clip(a, 0, 1)`.

Сравните на `n = 10^6`. Посчитайте, сколько элементов было изменено (`np.sum((a < 0) | (a > 1))`) — это полезная побочная статистика. 



```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

# данные
a = rng.normal(size=1_000_000)


# ── Способ 1: обычный цикл Python ──────────────────────────
def loop_update(arr):
    r = []
    for x in arr:
        if x < 0:
            r.append(0.0)
        elif x > 1:
            r.append(1.0)
        else:
            r.append(x)
    return r


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy_update(arr):
    return np.clip(arr, 0.0, 1.0)

# ── Сравнение ──────────────────────────────────────────────
r_loop,  t_loop  = measure(loop_update,  a)
r_numpy, t_numpy = measure(numpy_update, a)

print(f"цикл:   {t_loop*1000:10.2f} мс")
print(f"NumPy:  {t_numpy*1000:10.2f} мс")
print(f"ускорение: {t_loop / t_numpy:.1f}X")
print(f"результаты совпадают: {all(np.isclose(r_loop, r_numpy))}")

```

    цикл:       172.02 мс
    NumPy:        3.66 мс
    ускорение: 47.0X
    результаты совпадают: True
    

## Блок 2. Агрегации по осям (задачи 5–7)

**Задача 5. Сумма по строкам матрицы.**
Дан массив `matrix` формы `(n, 10)`, `n = 10^5`:
- цикл: `for i in range(n): s = 0; for j in range(10): s += m[i, j]; result[i] = s`;
- NumPy: `m.sum(axis=1)`.

Сравните время и SLOC. 




```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

# данные
m = rng.normal(size=1_000_000).reshape(-1, 10)


# ── Способ 1: обычный цикл Python ──────────────────────────
def loop_py(matrix):
    r = []
    for i in range(100_000): 
        s = 0
        for j in range(10):
            s += m[i, j]
        r.append(s)
    return r


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy(matrix):
    return matrix.sum(axis=1)

# ── Сравнение ──────────────────────────────────────────────
r_loop,  t_loop  = measure(loop_py,  m)
r_numpy, t_numpy = measure(numpy, m)

print(f"цикл:   {t_loop*1000:10.2f} мс")
print(f"NumPy:  {t_numpy*1000:10.2f} мс")
print(f"ускорение: {t_loop / t_numpy:.1f}X")
print(f"результаты совпадают: {all(np.isclose(r_loop, r_numpy))}")

```

    цикл:       238.07 мс
    NumPy:        1.65 мс
    ускорение: 144.0X
    результаты совпадают: True
    

**Задача 6. Среднее по столбцам и нормировка.**
Дан `matrix` формы `(n, 10)`:
- цикл: для каждого столбца вычислить среднее, потом вычесть;
- NumPy: `m - m.mean(axis=0)` (broadcasting).

Сравните.



```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

# данные
m = rng.normal(size=1_000_000).reshape(-1, 10)


# ── Способ 1: обычный цикл Python ──────────────────────────
def loop_py(matrix):
    res = matrix.copy()
    mean = []
    for j in range(10):
        s = 0
        for i in range(100_000): 
            s += matrix[i, j]
        mean.append(s / 100_000)
    for j in range(10):
        for i in range(100_000): 
            res[i, j] -= mean[j]
    return res


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy(matrix):
    return matrix - matrix.mean(axis=0)

# ── Сравнение ──────────────────────────────────────────────
r_loop,  t_loop  = measure(loop_py,  m)
r_numpy, t_numpy = measure(numpy, m)

print(f"цикл:   {t_loop*1000:10.2f} мс")
print(f"NumPy:  {t_numpy*1000:10.2f} мс")
print(f"ускорение: {t_loop / t_numpy:.1f}X")
print(f"результаты совпадают: {np.allclose(r_loop, r_numpy)}")

```

    цикл:       574.05 мс
    NumPy:        5.44 мс
    ускорение: 105.6X
    результаты совпадают: True
    

**Задача 7. Поиск максимума и его индекса.**
Дан `a` длины `10^6`:
- цикл: пройти, запомнить `max_val` и `max_idx`;
- NumPy: `a.max()`, `a.argmax()`.

Сравните.



```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

# данные
a = rng.normal(size=1_000_000)


# ── Способ 1: обычный цикл Python ──────────────────────────
def loop_py(arr):
    i_max = 0
    v_max = arr[0]
    for i, v in enumerate(arr):
        if v > v_max:
            v_max = v
            i_max = i
        
    return v_max, i_max


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy(arr):
    # так два сканирования массива
    # return arr.max(), arr.argmax()
    # немного ускорим
    i = arr.argmax()
    return arr[i], i

# ── Сравнение ──────────────────────────────────────────────
r_loop,  t_loop  = measure(loop_py,  a)
r_numpy, t_numpy = measure(numpy, a)

print(f"цикл:   {t_loop*1000:10.2f} мс")
print(f"NumPy:  {t_numpy*1000:10.2f} мс")
print(f"ускорение: {t_loop / t_numpy:.1f}X")
print(f"результаты совпадают: {np.allclose(r_loop, r_numpy)}")

```

    цикл:       100.59 мс
    NumPy:        0.25 мс
    ускорение: 399.3X
    результаты совпадают: True
    

## Блок 3. Фильтрация и маски (задачи 8–10)

**Задача 8. Фильтрация по порогу.**
Дан `a` длины `10^6`:
- цикл: `[x for x in a if x > 0]` (список Python);
- NumPy: `a[a > 0]`.

Сравните время и память.



```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

# данные
a = rng.normal(size=1_000_000)


# ── Способ 1: обычный цикл Python ──────────────────────────
def list_py(arr):
    return [x for x in arr if x > 0]


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy(arr):
    return arr[arr > 0]

# ── Сравнение ──────────────────────────────────────────────
r_loop,  t_loop  = measure(list_py,  a)
r_numpy, t_numpy = measure(numpy, a)

print(f"цикл:   {t_loop*1000:10.2f} мс")
print(f"NumPy:  {t_numpy*1000:10.2f} мс")
print(f"ускорение: {t_loop / t_numpy:.1f}X")
print(f"результаты совпадают: {np.allclose(r_loop, r_numpy)}")

```

    цикл:       132.92 мс
    NumPy:        7.40 мс
    ускорение: 18.0X
    результаты совпадают: True
    

**Задача 9. Замена по маске (in-place).**
Дан `a` длины `10^6`. Замените все отрицательные на их модуль:
- цикл: `for i in range(n): if a[i] < 0: a[i] = -a[i]`;
- NumPy: `a[a < 0] *= -1` (или `np.abs(a, out=a)`).

Сравните. 



```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

# данные
a = rng.normal(size=1_000_000)


# ── Способ 1: обычный цикл Python ──────────────────────────
def loop_py(arr):
    for i in range(len(arr)):
        if arr[i] < 0:
            arr[i] = -arr[i]


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy(arr):
    arr[arr < 0] *= -1

# ── Сравнение ──────────────────────────────────────────────
r_loop = a.copy()
_,  t_loop  = measure(loop_py,  r_loop)
r_numpy = a.copy()
_, t_numpy = measure(numpy, r_numpy)

print(f"цикл:   {t_loop*1000:10.2f} мс")
print(f"NumPy:  {t_numpy*1000:10.2f} мс")
print(f"ускорение: {t_loop / t_numpy:.1f}X")
print(f"результаты совпадают: {np.allclose(r_loop, r_numpy)}")

```

    цикл:       151.43 мс
    NumPy:        1.37 мс
    ускорение: 110.8X
    результаты совпадают: True
    

**Задача 10. Комбинированная маска.**
Дан `a` длины `10^6`. Выберите элементы, для которых `(a > -1) & (a < 1)`:
- цикл: `if -1 < x < 1`;
- NumPy: `a[(a > -1) & (a < 1)]`.

Сравните. Обратите внимание: в Python условие `-1 < x < 1` — читаемое, а в NumPy нужно `(a > -1) & (a < 1)` — скобки обязательны, иначе `ValueError`/неверный результат. 



```python
# инициализация генератора псевдослучайных чисел
rng = np.random.default_rng(42)

# данные
a = rng.normal(size=1_000_000)


# ── Способ 1: обычный цикл Python ──────────────────────────
def loop_py(arr):
    res = []
    for x in arr:
        if -1 < x < 1:
            res.append(x)
    return res


# ── Способ 2: NumPy ────────────────────────────────────────
def numpy(arr):
    return arr[(arr > -1) & (arr < 1)]

# ── Сравнение ──────────────────────────────────────────────
r_loop,  t_loop  = measure(loop_py,  a)
r_numpy, t_numpy = measure(numpy, a)

print(f"цикл:   {t_loop*1000:10.2f} мс")
print(f"NumPy:  {t_numpy*1000:10.2f} мс")
print(f"ускорение: {t_loop / t_numpy:.1f}X")
print(f"результаты совпадают: {np.allclose(r_loop, r_numpy)}")

```

    цикл:       161.02 мс
    NumPy:        7.72 мс
    ускорение: 20.8X
    результаты совпадают: True
    
