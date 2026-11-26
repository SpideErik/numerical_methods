import timeit
import matplotlib.pyplot as plt
import numpy as np
import tracemalloc

stmt1 = "out = []\nfor i in range(N):\n    out.append(i*i)"
stmt2 = "out = [i*i for i in range(N)]"
stmt3 = "out = list(map(lambda i: i*i, range(N)))"

x = 50_000, 200_000, 800_000

y = np.zeros((3, 2, len(x)), dtype=np.float64) # 3 способа, 2 метрики (время, память), len(x) измерений в каждом

for i, N in enumerate(x):
    for j, stmt in enumerate((stmt1, stmt2, stmt3)):
        # Замер времени
        times = timeit.repeat(stmt, globals={"N": N}, number=1, repeat=5)
        y[j, 0, i] = min(times) * 1000  # миллисекунды

        # Замер памяти
        tracemalloc.start()
        exec(stmt, {"N": N})
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        y[j, 1, i] = peak / (1024 * 1024)  # МБ

# Построение графиков
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

names = ["append", "list comprehension", "map + lambda"]
print(x)

# График времени
for i, name in enumerate(names):
    ax1.plot(x, y[i, 0, :], "o-", label=name)

ax1.set_title("Время создания списка")
ax1.set_xlabel("Количество элементов (N)")
ax1.set_ylabel("Время (мс)")
ax1.legend()
ax1.grid(True)

# График памяти
x_pos = range(len(y))
width = 0.25

for i, name in enumerate(names):
    ax2.bar(
        [p + (i - 1) * width for p in x_pos],
        y[i, 0, :],
        width,
        label=name,
    )

ax2.set_title("Пиковое потребление памяти")
ax2.set_xlabel("Размер списка")
ax2.set_ylabel("Память (МБ)")
ax2.set_xticks(list(x_pos))
ax2.set_xticklabels([f"N={N}" for N in x])
ax2.legend()
ax2.grid(axis="y")

plt.tight_layout()

plt.savefig("hw2_squares.png", dpi=150, bbox_inches="tight")
plt.show()
