import timeit
import matplotlib.pyplot as plt
import numpy as np

stmt = """
-1 in data
"""        

x = 100, 1_000, 10_000, 100_000 # ось x
y = np.zeros((3, len(x)), dtype=np.float64)  # 3 способа, len(x) измерений в каждом

for i, n in enumerate(x):
    data_list = list(range(n))
    data_set = set(range(n))
    data_dict = {i: i for i in range(n)}
    times = [
        timeit.repeat(stmt, globals={"data": data}, number=1000, repeat=5)
        for data in (data_list, data_set, data_dict)
    ]
    y[:,i]=([min(t) * 1000 for t in times])  # время в мкс на одно измерение  (*1e6 / 1000)
    
# Выодим таблицу
# выводит таблицу: `n`, время для каждой коллекции, во сколько раз `set` и `dict` быстрее `list`

t = f"| {'n':>7} | {'t list мкс'} | {'t set мкс'} | {'t dict мкс'} | {'set быстрее в'} | {'dict быстрее в'} |"
print(t)
print("|".join("-" * len(col) for col in t.split('|')))
    
for i, n in enumerate(x):
    print (f"| {n:7.0e} | {y[0, i]:10.3e} | {y[1, i]:9.6f} | {y[2, i]:10.6f} | {y[0, i] / y[1, i]:13.0f} | {y[0, i] / y[2, i]:14.0f} |")

# Создаём Figure с одной Axes
fig, ax = plt.subplots(figsize=(8, 5))

# логарифмическая шкала с сеткой
ax.set_xscale("log")
ax.set_yscale("log")
ax.grid(True, which="both", alpha=0.2)

# Рисуем две линии с разными стилями
ax.plot(x, y[0], label="список", color="red", linestyle="--", linewidth=2)
ax.plot(x, y[1], label="множество", color="blue", linestyle="-", linewidth=2)
ax.plot(x, y[2], label="словарь", color="green", linestyle="-.", linewidth=2)

# Подписи осей и заголовок
ax.set_xlabel("Размер данных (n)", fontsize=12)
ax.set_ylabel("Время (мкс)", fontsize=12)
ax.set_title("проверки вхождения в коллекцию", fontsize=14, fontweight="bold")

# Легенда — какая линия что означает
ax.legend(fontsize=10, loc="upper left")

plt.tight_layout()  # автоматически подгоняет отступы

plt.savefig("hw1_search.png", dpi=150, bbox_inches="tight")
plt.show()
